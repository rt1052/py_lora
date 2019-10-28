#coding=utf-8

from socket import *
from threading import *
from sqlite3 import *
from Queue import *
from time import *
from datetime import *
import json

# 本地调用
from global_var import *


# {"state": "on", "cmd": "SET STATE REQUEST", "id": 1}
# {cmd": "GET ALL STATE"}
def analyse_json_frame(sock, fd, buf):
    dict = json.loads(buf)

    cmd = dict["cmd"]

    # 获取所有设备状态
    if cmd == "GET ALL STATE":
        tmp = {"type": "dev list", "dev": g_var.dev_arr}
        # 通过tcp发送
        # sock.send(json.dumps(tmp, indent=1))
        sock.send(json.dumps(tmp, indent=1))
    else:
        state = dict["state"]
        arr = []
        # 帧头
        arr.append(0x42)
        # 帧长
        arr.append(0x05) # 0x06
        # arr.append(fd)
        arr.append(dict["id"])

        if cmd == "SET STATE REQUEST":
            arr.append(0x1)
        elif cmd == "GET STATE REQUEST":
            arr.append(0x3)
        elif cmd == "GET SENSOR REQUEST":
            arr.append(0x5)

        if state == "on":
            arr.append(0)
        elif state == "off":
            arr.append(1)
            
        print(arr)  
        g_var.lora_queue.put(arr)


def tcp_client(sock, info):
    print(sock, 'connected')
    fd = info['fd']
    queue = info['queue']
    while True:
        try:
            # 接收tcp数据
            buf = sock.recv(1024)
            # 连接已断开
            if buf == b"":
                print(sock, 'disconnected[1]')
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

        except socket.error:
            print(sock, 'disconnected[2]')
            # 从客户端队列中删除
            for i in g_var.cli_arr:
                if i['fd'] == fd:
                    g_var.cli_arr.remove(i)            
            sock.close()

        # 接收lora数据
        if not queue.empty():
            sock.send(queue.get())


def thread_tcp():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    # 设置ip和端口，''表示本地ip
    srv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    srv_sock.bind(('', 54301))
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


