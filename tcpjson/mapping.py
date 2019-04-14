import base64
import struct
import matplotlib.pyplot as plt

m = "AAAAAAAAZABk0ssAVUDTAAFaw6qUAAVU0QDEqqQABqXQAAHDqqmkABalqNAApsWqpsKqgM8AAsiqkM8ACprHqpDQAArHqpDQACrFqpmqkNQAFVqhqpDWAAFVUND4AA=="
track = "AQkhADIxNjEoMSgwOTA4MDgvNS81MisyKzNMM0w0LjQuNUw1TDZINkg3TDdJN0kyQjJDMkMxRjFFMUUwQzBEMEQ2PjZENg=="
inp = base64.b64decode(m)
d = struct.unpack('<' + 'B' * (len(inp)), inp)
# print(d[9:])
full = [['.' for i in range(100)] for j in range(110)]
akt = 0
i = 0


def placebyte(by):
    pair = by
    if pair & 0b10 == 0b10:
        # white
        full[((akt + 3) // 100)][((akt + 3) % 100)] = '_'
    elif pair & 0b01 == 0b01:
        # white
        full[((akt + 3) // 100)][((akt + 3) % 100)] = '0'
    pair = by >> 2
    if pair & 0b10 == 0b10:
        # white
        full[((akt + 2) // 100)][((akt + 2) % 100)] = '_'
    elif pair & 0b01 == 0b01:
        # white
        full[((akt + 2) // 100)][((akt + 2) % 100)] = '0'
    pair = by >> 4
    if pair & 0b10 == 0b10:
        # white
        full[((akt + 1) // 100)][((akt + 1) % 100)] = '_'
    elif pair & 0b01 == 0b01:
        # white
        full[((akt + 1) // 100)][((akt + 1) % 100)] = '0'
    pair = by >> 6
    if pair & 0b10 == 0b10:
        # white
        full[(akt // 100)][(akt % 100)] = '_'
    elif pair & 0b01 == 0b01:
        # white
        full[(akt // 100)][(akt % 100)] = '0'


while i < len(d):
    if i >= 9:
        # header
        if d[i] & 0b11000000 == 0b11000000:
            # run length
            # print("rle")
            mul = d[i] & 0b00111111
            # print("single mul",mul, d[i+1])
            if d[i + 1] & 0b11000000 == 0b11000000:
                # double encoded
                # print("double mul")
                i += 1
                mul <<= 6
                mul |= (d[i] & 0b00111111)
            # print("mul", mul)
            # repeat byte afterwards
            # print("repeat", d[i+1])
            for rep in range(mul):
                placebyte(d[i + 1])
                akt += 4
            # print("akt at ",akt)
            i += 1
        else:
            # print(d[i])
            placebyte(d[i])
            # print(b)
            akt = akt + 4
    i += 1

print("\n".join(["".join(map(str,fline)) for fline in full]))

wallx = []
wally = []
floorx = []
floory = []
for idy,l in enumerate(full):
    for idx,r in enumerate(l):
        if r == '0':
            wallx.append(idx)
            wally.append(idy)
        if r == '_':
            floorx.append(idx)
            floory.append(idy)

inp = base64.b64decode(track)
path = struct.unpack('<' + 'b'*(len(inp)-4), inp[4:])

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
fig.gca().invert_yaxis()
ax.scatter(wallx,wally,s=40)
ax.scatter(floorx,floory, s=30)
ax.set_aspect('equal')
ax.plot(path[0::2],path[1::2], color='green',linewidth=3.0)
plt.show()