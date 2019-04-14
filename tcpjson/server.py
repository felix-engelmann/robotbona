import socketserver

import struct
import json


class JSONTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def _build_response(self,magic, payload, seq, flag = b'\x00\x00\x00\x00'):
        lenstr = struct.pack("<i", len(payload) + 20)
        #print(lenstr)
        lenstr += (magic + b'\x01\x00\x00\x00')
        seqstr = struct.pack("<i", seq)
        seqstr += flag
        lenstr += seqstr
        lenstr += payload

        return lenstr

    def _build_first_ack(self, payload, seq):

        restring = json.dumps(payload).encode("ascii")
        restring += b'\x0a'

        return self._build_response(b'\x11\x00\xc8\x00', restring, seq)

    def _build_ack(self, payload, seq):

        restring = json.dumps(payload).encode("ascii")
        restring += b'\x0a'
        return self._build_response(b'\x19\x00\xc8\x00', restring, seq)


    def _build_stub(self, seq):
        stub = self._build_response(b'\x11\x01\xc8\x00', b'', seq, flag=b'\xe7\x03\x00\x00')
        print("sub:", stub)
        return stub


    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            # read length of package
            self.data = self.request.recv(4)
            if len(self.data) < 4:
                print("error, wait for more")
                return
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            length = struct.unpack("<i", self.data)[0]
            print("listen for length:", length)
            while len(self.data) < length:
                self.data += self.request.recv(length-len(self.data))

            print("all data received")

            sequence = struct.unpack("<i", self.data[12:16])[0]
            try:
                payload = json.loads(self.data[20:])
            except json.decoder.JSONDecodeError:
                payload = None
            print(payload)
            with open("dump.json",'a+') as f:
                f.write(self.data[20:].decode('ascii')+'\n')

            print("sequence:",sequence)

            respayload = {"msg":"","result":0 ,"time":"2019-02-17-23-51-08","version":""}

            # first packet:
            if payload and ( "value" in payload ) and ( "token" in payload["value"] ):
                print("return first response with time")
                self.request.sendall(self._build_first_ack(respayload, sequence))
            # stub
            elif length == 20:
                print("return stub")
                self.request.sendall(self._build_stub(sequence))
            else:
                print("ack")
                del respayload["time"]
                self.request.sendall(self._build_ack(respayload, sequence))

            # just send back the same data, but upper-cased
            #self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 20008

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), JSONTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()