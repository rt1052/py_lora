

info = []
dict = {}
dict["name"] = 'qian'
dict['age'] = '8'
info.append(dict)
	
dict = {}
dict["name"] = 'yu'
dict['age'] = '18'
info.append(dict)	

dict = {}
dict["name"] = 'heng'
dict['age'] = '28'
info.append(dict)	

for i in info:
	if i['name'] == 'yu':
	    info.remove(i)

for i in info:
	print i
	