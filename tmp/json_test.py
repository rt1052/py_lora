#coding=utf-8

import json

data = [
    {
        "school":"middle",
        "name":"smith",
        "age":22,
    },
]

json_data = json.dumps(data)
print(json_data)
dict_data = json.loads(json_data)
print(dict_data)