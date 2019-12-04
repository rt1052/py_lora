#coding=utf-8

from Queue import *


class g_var():
	# 客户端信息
	cli_arr = []
	alarm_arr = []
	# 设备信息
	dev_arr = []	
	lora_queue = Queue()

	polling_fd = 1
	alarm_fd = 2
	update_fd = 100
