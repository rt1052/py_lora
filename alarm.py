#coding=utf-8


def alarm_init():
    db = connect('lora.db')
    dbc = db.cursor()

    # 建立传感器表
    #dbc.execute('create table dht11(Time VARCHAR(12), humi REAL, temp REAL);')
    #dbc.execute('insert into dht11 values(datetime(\'now\', \'localtime\'), 50, 28.6);')

    # 建立闹钟表
    
    dbc.execute('create table alarm(Time VARCHAR(12), id INTEGER, dat INTEGER);')
    dbc.execute('insert into alarm values(TIME("19:49:00"), 3, 0);')
    dbc.execute('insert into alarm values(TIME("08:00:00"), 3, 1);')

    dbc.execute('insert into alarm values(TIME("22:30:00"), 2, 1);')
    dbc.execute('insert into alarm values(TIME("07:42:00"), 2, 0);')
    

    # 从数据库中读取闹钟信息
    data = dbc.execute("SELECT * from alarm")
    for row in data:
        # print row[0], row[1], row[2], row[3]
        info = {}
        alarm = datetime.strptime('16:47:00', '%H:%M:%S')
        # 将时间转换成datetime格式
        info['time'] = row[0]
        # datetime.strptime(row[0], '%H:%M:%S')
        info['id'] = row[1]
        info['dat'] = row[2]
        alarm_arr.append(info)

    dbc.close()
    db.commit()
    db.close()           


def thread_alarm():
    alarm_init()
    # 闹钟超时时间
    delta = timedelta(minutes = 1)

    while True:
        # 响应闹钟事件
        for i in alarm_arr:
            alarm = datetime.strptime(i['time'], '%H:%M:%S')
            # 获取当前系统时间
            str = strftime("%H:%M:%S", localtime()) 
            now = datetime.strptime(str, "%H:%M:%S")

            if now < alarm:
                pass
                # print alarm - now 
            elif (now-alarm) < delta:
                # 发送lora数据
                pass
            else:
                # 超时则删除闹钟
                alarm_arr.remove(i)

        sleep(10)


        # 每隔10分钟采集设备信息
        # lora_queue.put(str)

        # 根据闹钟时间发送lora数据

        # 响应客户端的闹钟设置、查询请求
