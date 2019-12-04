#coding=utf-8

from tcp import *
from threading import *
import logging
import logging.handlers
import struct


# 本地调用
from global_var import *
from tcp import *
from lora import *
from alarm import *


def thread_user():
    while True:
        msg = raw_input('user#')
        # 按enter键
        if msg == '':
            print('user#')
        elif msg == "lsd":
        	for i in g_var.dev_arr:
        		print(i["id"], i["state"], i["humidity"], i["temperature"])
        elif msg == "lsc":
            for i in g_var.cli_arr:
                print(i["fd"], i["host"])
        elif msg == "lsa":
            for i in g_var.alarm_arr:
                print(i)
        elif msg == "update":
            # 更新设备固件线程
            update_thread = Thread(target = thread_update)
            update_thread.start()            
        else:
            print('unknow cmd')


def thread_update():
    # 保存新连接的信息
    queue = Queue()
    info = {}
    info['fd'] = g_var.update_fd
    info['host'] = "update"
    info['queue'] = queue
    g_var.cli_arr.append(info)

    """
    每2秒发送一次更新请求帧，直到有响应，
    如果10秒内没有响应则退出
    """
    for i in range(0, 10):
        lora_frame_create(g_var.update_fd, 1, "UPDATE START", None)
        # 接收lora数据
        try:
            cnt = queue.get(timeout = 2)
            if (cnt == 0):
                break
        except:
            if (i > 5):
                g_var.cli_arr.remove(info)
                return            

    # 读取bin文件
    file = open("bin/lora.bin", "rb")
    data = file.read()
    data_len = len(data)
    # 每次发送的数据长度
    step = 100

    """
    根据终端返回的序号，把对应的数据发送给终端
    """
    while True:
        try:
            # 接收lora数据，超时则退出线程
            cnt = queue.get(timeout = 10)
            start = cnt * step
            end = (cnt+1) * step
            # 全部数据发送完毕则退出
            if (start > data_len):
                break
            elif (end > data_len):
                end = data_len            

            buf = data[start:end]
            arr = []
            arr.append(cnt)
            arr.extend(struct.unpack('B'*len(buf), buf))
            lora_frame_create(g_var.update_fd, 1, "UPDATE DATA", arr)           
        except:
            break

    file.close()    
    g_var.cli_arr.remove(info)  


# 每十分钟查询设备
def thread_polling():
    # 保存新连接的信息
    info = {}
    info['fd'] = g_var.polling_fd
    info['host'] = "polling"
    info['queue'] = Queue()
    g_var.cli_arr.append(info)

    while True:
        logging.info("polling")
        for i in range(1, 5):
            lora_frame_create(g_var.polling_fd, i, "GET STATE REQUEST", None)
            lora_frame_create(g_var.polling_fd, i, "GET SENSOR REQUEST", None)
        sleep(30*60)          

    # 将传感器数据存入数据库
    # 建立传感器表
    #dbc.execute('create table dht11(Time VARCHAR(12), humi REAL, temp REAL);')
    #dbc.execute('insert into dht11 values(datetime(\'now\', \'localtime\'), 50, 28.6);')


def log_init():

    logging.basicConfig()

    # when表示间隔单位，设成MIDNIGHT在零点刷新
    # interval表示时间间隔
    # 日志文件超过backupCount就会删除最早的日志，设成0就不会删除
    fileshandle = logging.handlers.TimedRotatingFileHandler("/var/log/lora/hc_server", when='MIDNIGHT', interval=1, backupCount=0)
    # 日志文件后缀
    fileshandle.suffix = "%Y-%m-%d"
    # 输出级别
    fileshandle.setLevel(logging.DEBUG)
    # 如果没有下面这句，前面设置的输出级别不会生效
    logging.root.setLevel(logging.NOTSET)
    # 日志内容和时间格式
    formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fileshandle.setFormatter(formatter)
    # 添加句柄
    logging.getLogger('').addHandler(fileshandle)


if __name__ == "__main__": 

    log_init()
    logging.info("start")

    # 用户输入线程
    usr_thread = Thread(target = thread_user)
    usr_thread.start()

    # 闹钟线程
    alarm_thread = Thread(target = thread_alarm)
    alarm_thread.start()

    # 模拟lora收发
    lora_thread = Thread(target = thread_lora)
    lora_thread.start()  

    # tcp线程      
    tcp_thread = Thread(target = thread_tcp)
    tcp_thread.start() 

    # 轮询线程
    polling_thread = Thread(target = thread_polling)
    polling_thread.start()
