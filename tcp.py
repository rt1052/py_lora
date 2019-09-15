#coding=utf-8

from socket import *
from threading import *
from sqlite3 import *
from Queue import *
from time import *
from datetime import *


cli_arr = []
alarm_arr = []
lora_queue = Queue()

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
                print(sock, 'disconnected')

                for i in cli_arr:
                    if i['fd'] == fd:
                        cli_arr.remove(i)

                sock.close()
                break
            else:
                # 为收到的数据添加文件标识符
                str = buf[0:2] + chr(fd) + buf[2:]
                # 添加到lora消息队列
                lora_queue.put(str)

        except timeout as e:
            pass

        # 接收lora数据
        if not queue.empty():
            sock.send(queue.get())


def thread_user():
    while True:
        msg = raw_input('user#')
        # 按enter键
        if msg == '':
            print('user#')
        elif msg == 'ls':
            for i in cli_arr:
                print i['fd'],i['host']
        elif msg == 'lsa':
            for i in alarm_arr:
                print i
        else:
            print('unknow cmd')


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


def thread_lora():
    while True:
        if not lora_queue.empty():
            str = lora_queue.get()
            
            for i in cli_arr:
                # 找到对应的tcp连接
                if str[2] == chr(i['fd']):
                    i['queue'].put(str)
        else:
            # 休眠10ms
            sleep(0.01)


def thread_tcp():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    # 设置ip和端口，''表示本地ip
    srv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    srv_sock.bind(('', 12345))
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
        cli_arr.append(info)

        # 为连接创建线程，因为只有一个arg参数，所以要以逗号结尾
        cli_thread = Thread(target = tcp_client,
                            args = (cli_sock, info))
        cli_thread.start()

    srv_sock.close()


if __name__ == "__main__": 

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
