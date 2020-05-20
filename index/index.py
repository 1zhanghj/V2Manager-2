from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from index.models import V2rayConfig
import os
import re
import uuid

def index(request):
    js = ['index.js']
    content = {}
    content['title'] = "Home"
    content['scripts'] = js
    return render(request, 'config.html', content)

def v2rayHas(request):
    sqlreslist = V2rayConfig.objects.all()
    res = {}
    res['code'] = 1
    res['data'] = {}
    v2ray = {}
    status = {}
    if len(sqlreslist) == 0:
        v2ray = False

    else:
        v2ray['has'] = True
        v2ray['V2rayCorePath'] = sqlreslist[0].Path
        v2ray['V2rayLogPath'] = sqlreslist[0].Log
        v2ray['LogLevel'] = sqlreslist[0].Level
        v2ray['Port'] = sqlreslist[0].Port
        v2ray['Portocol'] = sqlreslist[0].Portocol
        v2ray['DataPortocol'] = sqlreslist[0].DataPortocol
        v2ray['UUID'] = sqlreslist[0].UUID

        has = os.popen('ls {}/v2ray'.format(sqlreslist[0].Path)).readlines()
        if re.search(r'No such file or directory', has[0]) != None:
            v2ray['has'] = False
            status = None
        else:
            v2raystatus = os.popen('sudo systemctl status v2ray').readlines()
            status['Active'] = re.search(r'running|exited|waiting', v2raystatus[2]).group()
            status['Date'] = re.search(r'\d+\-\d+\-\d+ \d+:\d+:\d+ \w+', v2raystatus[2]).group()
    res['data']['status'] = status              
    res['data']['v2ray'] = v2ray
    res = JsonResponse(res)
    return res

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
    
    row = list(V2rayConfig.objects.filter(UUID = request.GET['UUID']))
    if len(row) == 0:
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
        V2rayConfig.objects.filter(UUID = request.GET['UUID']).update(
            UUID = request.GET['UUID'],
            Path = request.GET['V2rayCorePath'],
            Log = request.GET['V2rayLogPath'],
            Level = request.GET['LogLevel'],
            Port = request.GET['Port'],
            Portocol = request.GET['Portocol'],
            DataPortocol = request.GET['DataPortocol']
        )
    
    res['data']['msg'] = "OK"
    res = JsonResponse(res)
    return res