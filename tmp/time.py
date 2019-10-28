from datetime import *
from time import *



alarm = datetime.strptime('16:47:00', '%H:%M:%S')
delta = timedelta(minutes = 1)

while True:
	str = strftime("%H:%M:%S", localtime()) 
	now = datetime.strptime(str, "%H:%M:%S")

	if now < alarm:
		print alarm - now 
	elif (now-alarm) < delta:
		print 'delay'
	else:
		print 'time out'
		break

	sleep(1)