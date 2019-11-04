#coding=utf-8

from sqlite3 import *
from time import *
from datetime import *
import logging
import logging.handlers

# 本地调用
from global_var import *
from lora import *


# 从数据库读出闹钟
def alarm_read_db(id):
    db = connect('info.db')
    dbc = db.cursor()

    # 没有id参数则读取所有闹钟信息
    if id == None:
        data = dbc.execute("SELECT * from alarm")
    else:

        data = dbc.execute("SELECT where id = " + str(id) +" from alarm")

    arr = []
    # 将闹钟信息存入数组
    for row in data:
        info = {}
        alarm = datetime.strptime('16:47:00', '%H:%M:%S')
        # 将时间转换成datetime格式
        info['time'] = row[0]
        # datetime.strptime(row[0], '%H:%M:%S')
        info['id'] = row[1]
        info['state'] = row[2]
        arr.append(info)

    dbc.close()
    db.close()
    return arr  


# 将闹钟写入数据库，每次存入一条
def alarm_write_db(id, time, state):
    db = connect('info.db')
    dbc = db.cursor()

    # 如果闹钟表不存在，则创建
    dbc.execute("create table if not exists alarm(Time VARCHAR(12), id INTEGER, dat VARCHAR(5));")

    values = [(time, str(id), state)]
    dbc.executemany("insert into alarm values (?,?,?)", values)

    dbc.close()
    db.commit()
    db.close()


# 删除闹钟
def alarm_delete(id, time):
    pass


def alarm_test():
    alarm_write_db(3, "22:00:00", "on")
    alarm_write_db(3, "08:00:00", "off")


def thread_alarm():
    # alarm_test()
    g_var.alarm_arr = alarm_read_db(None)
    # 闹钟超时时间
    delta = timedelta(minutes = 1)
    zero = datetime.strptime("00:00:00", "%H:%M:%S")

    queue = Queue()
    # 保存新连接的信息
    info = {}
    info['fd'] = g_var.alarm_fd
    info['host'] = "alarm"
    info['queue'] = queue
    g_var.cli_arr.append(info)

    while True:
        # 获取当前系统时间
        str = strftime("%H:%M:%S", localtime()) 
        now = datetime.strptime(str, "%H:%M:%S")

        # 每天00:00重新从数据库读取闹钟
        if ((now > zero) and (now - zero) < delta):
            logging.info("alarm reset")
            g_var.alarm_arr = alarm_read_db(None)
            # 跳过一分钟
            sleep(60)

        # 接收lora数据
        while not queue.empty():
            data = queue.get()
            dict = json.loads(data)
            dev = dict["dev"]
            # 删除对应的闹钟
            for i in g_var.alarm_arr:
                # 检查id和状态
                if (dev["id"] == i["id"] and dev["state"] == i["state"]):
                    # 检查时间
                    if (now > alarm and (now-alarm) < delta):
                        g_var.alarm_arr.remove(i)
                        logging.info("alarm get: %s", i)
                        break

        # 响应闹钟事件
        for i in g_var.alarm_arr:
            alarm = datetime.strptime(i['time'], '%H:%M:%S')

            if now < alarm:
                pass
            elif (now-alarm) < delta:
                logging.info("alarm post: %s", i)
                # 发送lora数据
                lora_frame_create(g_var.alarm_fd, i["id"], "SET STATE REQUEST", i["state"])
            else:
                logging.info("alarm timeout: %s", i)
                # 超时则删除闹钟
                g_var.alarm_arr.remove(i)

        sleep(10)

        # 响应客户端的闹钟设置、查询请求
