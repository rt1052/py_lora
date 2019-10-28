import struct
import json

arr = [0x42, 0x1, 0x2]

#tt = struct.pack('3B', arr[0], arr[1], arr[2])
#tt = struct.pack('3B', for i in arr)

tt = struct.pack('B' * len(arr), *arr)
print(tt)