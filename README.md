# V2Manager

V2Manager全称V2ray Manager，是一款用于服务器端的V2ray管理应用。

V2Manager基于Django(Python)开发，以Web为主要形式的服务器应用，支持可视化操作、配置V2ray，方便新手使用。

## 环境要求

- Linux系统

- Python 3.6.5 以上
- sqlite 3
- wget
- bash
- v2ray

## 安装

V2Manager采用命令行安装，从github下载发行包并解压。

运行以下代码初始化环境

```shell
# 进入解压好的文件夹V2Manager
$ cd V2Manager
$ sudo bash ./begin.sh
```

## 运行

安装好环境以后运行

```shell
$ sudo python3 manage.py runserver 0.0.0.0:<port> --insecure
```

- `<port>`是网站的访问端口，可以随意设置，但是请不要和其他进程的端口重复

## 访问

浏览器打开`http://<你的服务器IP>:<你刚刚设置好的访问端口>`

![result](/doc/img/result.png)