import sqlite3


db = sqlite3.connect('lora.db')
dbc = db.cursor()
dbc.execute('create table dht11(Time VARCHAR(12), humi REAL, temp REAL);')
dbc.execute('insert into dht11 values(datetime(\'now\', \'localtime\'), 50, 28.6);')
dbc.close()
db.commit()
db.close()