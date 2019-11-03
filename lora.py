#coding=utf-8

from socket import *
import json
import struct
import logging
import logging.handlers

# 本地调用
from global_var import *

# 接收到lora数据包并解析
def analyse_lora_frame(arr):
    """
    按照协议解析lora数据帧
    """
    fd = arr[2]
    id = arr[3]
    cmd = arr[4]
    state = None
    humidity = None

    # 如果是传感器信息
    if cmd == 0x06:
        # 测试用
        return None
        humidity = arr[5]
        temperature = arr[7] + arr[8]/10
    else:
        if arr[5] == 0x0:
            state = "on"
        elif arr[5] == 0x1:
            state = "off"

    """
    更新设备的开关状态和传感器信息，如果列表中未包含该设备，则添加设备
    """
    dev = None
    for i in g_var.dev_arr:
        # 根据id查找设备
        if i["id"] == id:
            dev = i
    # 设备不存在
    if dev == None:
        dict = {}
        g_var.dev_arr.append(dict)
        # 获取刚添加的列表元素
        dev = g_var.dev_arr[-1]
        dev["id"] = id
        dev["state"] = None
        dev["humidity"] = None
        dev["temperature"] = None

    if state != None:
        dev["state"] = state
    if humidity != None:
        dev["humidity"] = humidity
        dev["temperature"] = temperature

    """
    建立json数据帧
    """
    dict = {"type": "dev info", "dev": dev}
    if (cmd == 0x2 or cmd == 0x7):
        # 发给所有客户端
        send_to_client(None, json.dumps(dict, indent=1))
    else:
        # 发给指定客户端
        send_to_client(fd, json.dumps(dict, indent=1))


def send_to_client(fd, buf):
    # fd=None表示向所有tcp客户端发送数据
    if fd == None:
        for i in g_var.cli_arr:
            i["queue"].put(buf)
    else:
        for i in g_var.cli_arr:
            if i["fd"] == fd:
                i["queue"].put(buf)


def connect_to_server():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.connect(("192.168.0.43", 54301))
    # sock.connect(("127.0.0.1", 54301))
    logging.info("lora server connected")
    # 设置接收和发送超时200ms
    sock.settimeout(0.2)
    return sock


# 构建lora数据帧
def lora_frame_create(fd, id, cmd, state):
    arr = []
    # 帧头
    arr.append(0x42)
    # 帧长
    arr.append(0x06)
    arr.append(fd)
    arr.append(id)
    # 命令
    if cmd == "SET STATE REQUEST":
        arr.append(0x1)
    elif cmd == "GET STATE REQUEST":
        arr.append(0x3)
    elif cmd == "GET SENSOR REQUEST":
        arr.append(0x5)
    # 数据
    if state == "on":
        arr.append(0)
    elif state == "off":
        arr.append(1)
    elif state == None:
        arr.append(0)

    # 校验
    ck = 0
    for i in arr:
        ck += i
    arr.append(ck)
    # 加入发送队列
    g_var.lora_queue.put(arr)


def thread_lora():
    cli_sock = connect_to_server()

    while True:
        """
        接收lora数据帧，分析后发送到客户端
        """
        try:
            buf = cli_sock.recv(1024)
            if buf:
                # 将字符串转化为16进制数组
                arr = struct.unpack('B'*len(buf), buf) 
                logging.debug("lora recv: %s", arr)
                analyse_lora_frame(arr)
            elif buf == b"":
                logging.info("lora server disconnect[1]")
                cli_sock.close()
                cli_sock = connect_to_server()  

        except timeout as e:
            pass    

        except socket.error:
            logging.info("lora server disconnect[2]")
            cli_sock.close()
            cli_sock = connect_to_server()          

        """
        接收tcp客户端命令，转换成lora数据帧
        """
        if not g_var.lora_queue.empty():
            buf = g_var.lora_queue.get()
            logging.debug("lora send: %s", buf)
            # 将数组转换成字符串
            tmp = struct.pack('B'*len(buf), *buf)
            cli_sock.send(tmp)

        # 休眠10ms
        # sleep(0.01)
