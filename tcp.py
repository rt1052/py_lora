#coding=utf-8

from threading import *
from sqlite3 import *
from Queue import *
from time import *
from datetime import *
import socket
import json
import logging
import logging.handlers

from socket import error as socketError
import errno

# 本地调用
from global_var import *
from lora import *



# {"state": "on", "cmd": "SET STATE REQUEST", "id": 1}
# {cmd": "GET ALL STATE"}
def analyse_json_frame(sock, fd, buf):
    dict = json.loads(buf)

    cmd = dict["cmd"]

    # 获取所有设备状态
    if cmd == "GET ALL STATE":
        tmp = {"type": "dev list", "dev": g_var.dev_arr}
        # 通过tcp发送
        sock.send(json.dumps(tmp, indent=1))
    else:
        lora_frame_create(fd, dict["id"], dict["cmd"], dict["state"])  


def tcp_client(sock, info):
    logging.info("%s connected", info["host"])
    fd = info['fd']
    queue = info['queue']
    while True:
        try:
            # 接收tcp数据
            buf = sock.recv(1024)
            # 连接已断开
            if buf == b"":
                logging.info("%s disconnected[1]", info["host"])
                # 从客户端队列中删除
                for i in g_var.cli_arr:
                    if i['fd'] == fd:
                        g_var.cli_arr.remove(i)
                sock.close()
                break
            # 正常接收数据
            else:
                # 添加到lora消息队列
                analyse_json_frame(sock, fd, buf)

        except timeout as e:
            pass

        except socketError as e:
            if e.errno != errno.ECONNRESET:
                logging.info("%s disconnected[2]", info["host"])
                # 从客户端队列中删除
                for i in g_var.cli_arr:
                    if i['fd'] == fd:
                        g_var.cli_arr.remove(i)            
                sock.close()                
            else:
                logging.error("%s socket error", info["host"])           

        # 接收lora数据
        if not queue.empty():
            res = sock.send(queue.get())


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


