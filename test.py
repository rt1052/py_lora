#coding=utf-8

import struct
from Queue import *


def thread_update():
    print("file test")
    # 读取bin文件
    file = open("bin/lora.bin", "rb")
    data = file.read()


    cnt = 0
    step = 100
    start = cnt * step
    end = (cnt+1) * step - 1

    buf = data[start:end]
    arr = []
    # arr.append(cnt)
    arr.extend(struct.unpack('B'*len(buf), buf))

    #print(len(arr))


    a = [1, 2, 3, 4]
    b = a[0 : 2]
    print(b[0], b[1])
    print(len(b))

    """
    for i in range(0, 20):
        print("%02x" % data[i])
    """

    file.close()   



# thread_update()



for i in range(0, 10):
    print("r")