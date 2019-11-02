#coding=utf-8

from sqlite3 import *
from time import *
from datetime import *

# 本地调用
from global_var import *
from lora import *


# 从数据库读出闹钟
def alarm_read_db(id):
    db = connect('lora.db')
    dbc = db.cursor()

    # 没有id参数则读取所有闹钟信息
    if id == None:
        data = dbc.execute("SELECT * from alarm")
    else:
        data = dbc.execute("SELECT where id = " + str(id) +" from alarm")

    arr = []
    # 将闹钟信息存入数组
    for row in data:
        # print row[0], row[1], row[2], row[3]
        info = {}
        alarm = datetime.strptime('16:47:00', '%H:%M:%S')
        # 将时间转换成datetime格式
        info['time'] = row[0]
        # datetime.strptime(row[0], '%H:%M:%S')
        info['id'] = row[1]
        info['dat'] = row[2]
        arr.append(info)

    dbc.close()
    db.close()
    return arr  


# 将闹钟写入数据库，每次存入一条
def alarm_write_db(id, time, state):
    db = connect('lora.db')
    dbc = db.cursor()

    # 如果闹钟表不存在，则创建
    dbc.execute("create table if not exists alarm(Time VARCHAR(12), id INTEGER, dat VARCHAR(5));")

    data = [(time, str(id), state)]
    dbc.executemany('insert into alarm values (?,?,?)', data)

    dbc.close()
    db.commit()
    db.close()    


alarm_write_db(2, "16:12:00", "off")   



"""    
    # insert into alarm values(TIME("19:49:00"), 3, "on");
    dbc.execute("insert into alarm values(TIME(\"" + time + "\"), " + str(id) + ", " + state + ");")

    info = "insert into alarm values(TIME("19:49:00"), 3, "on");"

    cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
    
    into = "INSERT INTO scrapy_yilong2(title,author,comment,`time`) VALUES (%s,%s, %s, %s)"
    values = (item['title'],item['author'],item['comment'],item['time'])
    cur.execute(into, values)
""" 