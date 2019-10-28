#coding=utf-8

from tcp import *
from threading import *

# 本地调用
from global_var import *
from tcp import *
from lora import *


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


if __name__ == "__main__": 

    g_var.lora_queue = Queue();

    # 用户输入线程
    usr_thread = Thread(target = thread_user)
    usr_thread.start()

    # 闹钟线程
    # alarm_thread = Thread(target = thread_alarm)
    # alarm_thread.start()

    # 模拟lora收发
    lora_thread = Thread(target = thread_lora)
    lora_thread.start()  

    # tcp线程      
    tcp_thread = Thread(target = thread_tcp)
    tcp_thread.start() 
