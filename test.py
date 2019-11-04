#coding=utf-8

import socket
from threading import *
from sqlite3 import *
from Queue import *
from time import *
from datetime import *
import json
import logging
import logging.handlers

# 本地调用
from global_var import *
from lora import *


def tcp_client(sock, info):
    print("%s connected", info["host"])
    fd = info['fd']
    queue = info['queue']
    while True:
        try:
            # 接收tcp数据
            buf = sock.recv(1024)
            # 连接已断开
            if buf == b"":
                print("%s disconnected[1]", info["host"])
                # 从客户端队列中删除
                for i in g_var.cli_arr:
                    if i['fd'] == fd:
                        g_var.cli_arr.remove(i)
                sock.close()
                break
            # 正常接收数据
            else:
                # 添加到lora消息队列
                pass

        except timeout as e:
            pass

        except socket.error:
            print("%s disconnected[2]", info["host"])
            # 从客户端队列中删除
            for i in g_var.cli_arr:
                if i['fd'] == fd:
                    g_var.cli_arr.remove(i)            
            sock.close()

        res = sock.send("hello")
        print(res)
        sleep(1)



def thread_tcp():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    srv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 设置ip和端口，''表示本地ip
    srv_sock.bind(('', 54200))
    srv_sock.listen(5)

    while True:
        cli_sock, cli_addr = srv_sock.accept()
        # 设置接收和发送超时200ms
        cli_sock.settimeout(0.2)

        # 保存新连接的信息
        info = {}
        info['fd'] = cli_sock.fileno()
        info['host'] = cli_addr
        info['queue'] = Queue()
        g_var.cli_arr.append(info)

        # 为连接创建线程，因为只有一个arg参数，所以要以逗号结尾
        cli_thread = Thread(target = tcp_client,
                            args = (cli_sock, info))
        cli_thread.start()

    srv_sock.close()


thread_tcp()
