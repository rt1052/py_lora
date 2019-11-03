#coding=utf-8


import logging, logging.handlers
import time

''' TimedRotatingFileHandler构造函数声明 class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None) filename 日志文件名前缀 when 日志名变更时间单位 'S' Seconds 'M' Minutes 'H' Hours 'D' Days 'W0'-'W6' Weekday (0=Monday) 'midnight' Roll over at midnight interval 间隔时间，是指等待N个when单位的时间后，自动重建文件 backupCount 保留日志最大文件数，超过限制，删除最先创建的文件；默认值0，表示不限制。 delay 延迟文件创建，直到第一次调用emit()方法创建日志文件 atTime 在指定的时间（datetime.time格式）创建日志文件。 '''






def log_init():

    logging.basicConfig()

    # when表示间隔单位，设成MIDNIGHT在零点刷新
    # interval表示时间间隔
    # 日志文件超过backupCount就会删除最早的日志，设成0就不会删除
    fileshandle = logging.handlers.TimedRotatingFileHandler("log/hc_server", when='MIDNIGHT', interval=1, backupCount=0)
    # 日志文件后缀
    fileshandle.suffix = "%Y-%m-%d"
    # 输出级别
    fileshandle.setLevel(logging.DEBUG)
    # 日志内容和时间格式
    formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fileshandle.setFormatter(formatter)
    # 添加句柄
    logging.getLogger('').addHandler(fileshandle)


if __name__ == '__main__':
    log_init()

    arr = []
    arr.append(0x1)
    arr.append(0x2)


    dict = {"dev": arr}

    logging.warning("test %s", dict)