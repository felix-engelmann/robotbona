# Proscenic 790T

This document describes the journey of operating the vacuum robot Proscenic 790T without internet connection.

The presented insight resulted from many captured traces from the robot and the proscenic robot ab, which presents and controls the robot via a cloud.

For control, there are already many approaches and integrations in e.g. Homeassistant ( https://github.com/markomannux/pyproscenic , https://github.com/oskarn97/fhem-Proscenic ). This is performed with udp broadcast packets.

We were interested in tapping into the path and map the robot creates, which is also shown in the app.

## Setup


### Firewall

To run the robot without access to the internet, you have to add a firewall rule to your router, to block all packets from the robot to the internet.

### DNS

Without internet access, the robot tries to connect to various hosts, which we have to hijack to force the robot to talk to a server we control.

This is e.g. achieved by setting up a bind service and adding a `db.rpz` with the entries:
```
bl-app-eu.robotbona.com                     A    192.168.0.42
bl-im-eu.robotbona.com                      A    192.168.0.42


a1f59ahu0erdwx.iot.eu-west-1.amazonaws.com  A    192.168.0.42
```

## Registration

First, the robot queries the url
`http://bl-app-eu.robotbona.com/baole-web/common/getToken.do` to get a token. The response should look like
```
{"msg":"ok","result":"0","data":{
    "appKey":"67ce4fabe562405d9492cad9097e09bf",
    "deviceNo":"2de4a33c00c187",
    "token":"6ZbcjqEkokbI58yeS94Dt1C0YAsyxKwf"},
    "version":"1.0.0"}
```
where the `deviceNo` is provided in the POST data.

## Data

With this token, the robot proceeds to connect to a tcp service at `bl-im-eu.robotbona.com:20008`
There a very weird procotol is used, which enables JSON packets over TCP and is not HTTP.

### JSON Protocol

A packet has a 20 byte header and afterwards maybe an ascii encoded json object.

#### Header

The header is composed of
- \[0:3\] Length of the total packet in bytes
- \[4:7\] some magic bytes, probably flags etc.
- \[8:11\] allways b'\x01\x00\x00\x00'
- \[12:15\] sequence of packet
- \[16:19\] more flags
- \[20:\] json payload

#### State

The robot sends a first packet, which has to be answered specifically with an additional time in the payload.

For the rest of packets, the server has to reply with an ack package and the correct sequence number.

The robot also occasionally sends packets with empty payload, which also have to be acknowledged. This is most probably to keep the connection alive.

### Track and Map

The updates from the robot look generally like
```
{"version":"1.0","control":{"targetId":"0","targetType":"6","broadcast":"0"},"value":{"noteCmd":"101
","clearArea":"9","clearTime":"260","clearSign":"2019-02-17-23-51-08-1","clearModule":"3",
"map":
"AAAAAAAAZABk0ssAVUDTAAFaw6qUAAVU0QDEqqQABqXQAAHDqqmkABalqNAApsWqpsKqgM8AAsiqkM8ACprHqpDQAArHqpDQACrFqpmqkNQAFVqhqpDWAAFVUND4AA==",
"track":
"AQkhADIxNjEoMSgwOTA4MDgvNS81MisyKzNMM0w0LjQuNUw1TDZINkg3TDdJN0kyQjJDMkMxRjFFMUUwQzBEMEQ2PjZENg=="}}
```

The track is easily decoded by
```
track = base64.b64decode(data["track"])
path = struct.unpack('<' + 'b'*(len(track)-4), track[4:])
```
The first 4 bytes are length information and unknown. The rest is a list of 2 byte tuples with an x and y value.

For the map it is more evolved.
The header is 9 bytes long and specifies that the total area is 100 times 100 pixels. The rest is encoded byte wise.

We start at position (0,0) on the map.

If the byte has the highest two bits set, we are in repetition mode. The remaining 6 bits specify the number of repetitions. If the consecutive byte also starts with to bits set, the remaining 6 bits are also used to specify the number of repetitions. The first 6 bits are therefore shiftet left by 6. This is similar to variable length integer encoding.
The first byte not starting with 11 is then repeated so often.

A normal byte specifies 4 pixels by 2 bit each.
The occupation of the pixel is
- 00 for unknown (not explored)
- 10 floor
- 01 wall

## Tools

To facilitate building fancy applications and integrations, We built some tooling to get the data and process it.

### Webserver
There is a django project (overkill) which returns the token to the robot for initial contact.
Run it with
```
python3 manage.py runserver 0.0.0.0:8000
```

Running the server as root is not encouraged, and a firewall rule should be used:
```
iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 80 -j REDIRECT --to-port 8000
```

### JSON server

To interact with the robot over the weird JSON protocol, use the `tcpjson` tools by
```
python3 server.py
```
which dumps the received json messages in a file `dump.json`

The trace and map can be plotted with `tcpjson/mapping.py` matplotlib.