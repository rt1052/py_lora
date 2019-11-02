#coding=utf-8

from tcp import *
from threading import *

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
        else:
            print('unknow cmd')


# 每十分钟查询设备
def thread_polling():
    # 保存新连接的信息
    info = {}
    info['fd'] = g_var.polling_fd
    info['host'] = "polling"
    info['queue'] = Queue()
    g_var.cli_arr.append(info)

    while True:
        for i in range(1, 5):
            print(i, "request")
            lora_frame_create(g_var.polling_fd, i, "GET STATE REQUEST", None)
            lora_frame_create(g_var.polling_fd, i, "GET SENSOR REQUEST", None)
        sleep(10*60)          

    # 将传感器数据存入数据库
    # 建立传感器表
    #dbc.execute('create table dht11(Time VARCHAR(12), humi REAL, temp REAL);')
    #dbc.execute('insert into dht11 values(datetime(\'now\', \'localtime\'), 50, 28.6);')



if __name__ == "__main__": 

    g_var.lora_queue = Queue();

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
