from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from index.models import V2rayConfig, V2rayShadowsocks
import os
import psutil
import re
import uuid

def index(request):
    js = ['index.js']
    content = {}
    content['title'] = "Home"
    content['scripts'] = js
    content['Data'] = {}
    content['Status'] = {}

    # V2rayConfig
    v2rayconf = V2rayConfig.objects.all()
    if len(v2rayconf) != 0:
        content['v2raypath'] = v2rayconf[0].Path
        content['v2raylogpath'] = v2rayconf[0].Log
        content['loglevel'] = v2rayconf[0].Level
        content['v2rayport'] = v2rayconf[0].Port
        content['portocol'] = v2rayconf[0].Portocol
        content['UUID'] = v2rayconf[0].UUID
        content['Data']['portocol'] = v2rayconf[0].DataPortocol

        # V2rayLog
        logpath = v2rayconf[0].Log
        content['Status']['Log'] = ""
        if logpath != "":
            try:
                os.listdir(logpath)
            except:
                pass
            else:
                if 'access.log' in os.listdir(logpath) and (not os.path.isdir('{}/access.log'.format(logpath))):
                    log = os.popen('sudo tail -n 50 {}/access.log'.format(logpath)).readlines()
                    content['Status']['Log'] = ""
                    for l in log:
                        content['Status']['Log'] += l
    
    shadowsocksconf = V2rayShadowsocks.objects.all()
    if len(shadowsocksconf) != 0:
        content['Data']['ShadowsocksID'] = shadowsocksconf[0].ID
        content['Data']['ShadowsocksPwd'] = shadowsocksconf[0].Password

    # V2rayHas
    v2rayHas = True
    msg = ""
    try:
        os.listdir(v2rayconf[0].Path)
    except:
        v2rayHas = False
        msg = "该路径不存在"
    else:
        if not 'v2ray' in os.listdir(v2rayconf[0].Path):
            v2rayHas = False
            msg = "该路径下没有V2ray执行程序"
        elif os.path.isdir('{}/v2ray'.format(v2rayconf[0].Path)):
            v2rayHas = False
            msg = "该路径下的V2ray为文件夹，不符合要求"
    content['V2ray'] = {}
    content['V2ray']['Has'] = v2rayHas
    content['V2ray']['msg'] = msg

    # V2rayStatus
    
    v2raypid = None
    for pid in psutil.pids():
        if psutil.Process(pid).name() == 'v2ray':
            v2raypid = pid
            break

    if v2raypid == None:
        content['Status']['Active'] = 'Stop'
    else:
        content['Status']['Active'] = 'Running'

    print(ConfigJson(v2rayconf[0].Log, v2rayconf[0].Level, v2rayconf[0].Port, v2rayconf[0].DataPortocol, shadowsocksconf[0].ID, shadowsocksconf[0].Password, v2rayconf[0].Portocol, v2rayconf[0].UUID))

    return render(request, 'config.html', content)

def updateUUID(request):
    res = {}
    res['code'] = 1
    res['data'] = {}
    res['data']['uuid'] = str(uuid.uuid1())
    res = JsonResponse(res)
    return res

def updateConfig(request):
    res = {}
    res['code'] = 1
    res['data'] = {}
    
    if request.GET['UUID'] == '':
        res['code'] = 0
        res['data']['msg'] = "Error"
        return res
    
    v2rayconf = V2rayConfig.objects.all()
    if len(v2rayconf) == 0:
        V2rayConfig(
            UUID = request.GET['UUID'],
            Path = request.GET['V2rayCorePath'],
            Log = request.GET['V2rayLogPath'],
            Level = request.GET['LogLevel'],
            Port = request.GET['Port'],
            Portocol = request.GET['Portocol'],
            DataPortocol = request.GET['DataPortocol']
        ).save()
    else :
        V2rayConfig.objects.filter(UUID = v2rayconf[0].UUID).update(
            UUID = request.GET['UUID'],
            Path = request.GET['V2rayCorePath'],
            Log = request.GET['V2rayLogPath'],
            Level = request.GET['LogLevel'],
            Port = request.GET['Port'],
            Portocol = request.GET['Portocol'],
            DataPortocol = request.GET['DataPortocol']
        )

    shadowsocksconf = V2rayShadowsocks.objects.all()
    if len(shadowsocksconf) == 0:
        V2rayShadowsocks(
            ID = request.GET['ShadowsocksID'],
            Password = request.GET['ShadowsocksPwd']
        ).save()
    else:
        V2rayShadowsocks.objects.filter(ID = shadowsocksconf[0].ID).update(
            ID = request.GET['ShadowsocksID'],
            Password = request.GET['ShadowsocksPwd']
        )
    
    res['data']['msg'] = "OK"
    res = JsonResponse(res)
    return res

def ConfigJson(logpath, loglevel, port, dataportocol, ssID, ssPWD, portocol, uuid):
    if dataportocol == 'Shadowsocks':
        inboundsetting = """
        {
            "email": "{}",
            "method": "aes-128-gcm",
            "password": "{}",
            "level": 0,
            "ota": false,
            "network": "tcp"
        }
        """.format(ssID, ssPWD)
    else:
        inboundsetting = """
        "clients": [
            {
                "id": "{}",
                "alterId": 32
            }
        ]
        """.format(uuid)

    jsonstr = """
    {
        "log": {
            "access": "{}/access.log",
            "error": "{}/error.log",
            "loglevel": "{}"
        },
        "dns": {
        },
        "stats": {
        },
        "inbounds": [{
            "port": {},
            "portocol": "{}",
            "settings": {
                {}
            },
            "streamSettings": {
                "network": "{}",
                "security": "none",
                "tcpSettings": {
                }
            }
        }],
        "outbounds": [{
            "tag": "direct",
            "protocol": "freedom",
            "settings": {
            }
        },{
            "tag": "blocked",
            "protocol": "blackhole",
            "settings": {
            }
        }],
        "rounting": {
            "domainStrategy": "AsIs",
            "rules": [{
                "type": "field",
                "ip": [
                    "geoip:private"
                ],
                "outboundTag": "blocked"
            }]
        },
        "policy": {
        },
        "reverse": {
        },
        "transport": {
        }
    }
    """.format(logpath, loglevel, port, dataportocol, inboundsetting, portocol)
    return jsonstr