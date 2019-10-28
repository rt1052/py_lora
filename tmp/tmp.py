#coding=utf-8


'''
lora_buf = []

lora_buf.append(0x1)
lora_buf.append(0x2)

for i in lora_buf:
    print('%#x'%i)
'''



dev_arr = []


dict = {}
dict["id"] = 1
dict["state"] = "on"
dict["temperature"] = "21.6"
dict["humidity"] = "50"
dev_arr.append(dict)


dict = {}
dict["id"] = 2
dict["state"] = "off"
dict["temperature"] = "27.4"
dict["humidity"] = "80"
dev_arr.append(dict)

print(dev_arr[-1])

for i in dev_arr:
    print(i)

























'''
from Queue import *
from threading import Thread
import time

class Student(Thread):
    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue

    def run(self):
        while True:
            # 阻塞程序，时刻监听老师，接收消息
            msg = self.queue.get()
            # 一旦发现点到自己名字，就赶紧答到
            if msg == self.name:
                print("{}：到！".format(self.name))


class Teacher:
    def __init__(self, queue):
        self.queue=queue

    def call(self, student_name):
        print("老师：{}来了没？".format(student_name))
        # 发送消息，要点谁的名
        self.queue.put(student_name)


queue = Queue()
teacher = Teacher(queue=queue)
s1 = Student(name="小明", queue=queue)
s2 = Student(name="小亮", queue=queue)
s1.start()
s2.start()

print('开始点名~')
teacher.call('小明')
time.sleep(1)
teacher.call('小亮')
'''