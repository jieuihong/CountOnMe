from bluetooth import *
# bluetooth configuration
server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(3)

try:
    client, info = server.accept()
    print 'test2'

except KeyboardInterrupt:
    print("abort")
    server.close()
    exit()


def cli():
    return client
