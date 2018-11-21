from bluetooth import *
import time

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "99f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "Sample Server" , service_id=uuid, service_classes=[uuid, SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])

print("Waiting.....connection on RFCOMM channel %d", port)

client_socket, client_info = server_sock.accept()
print("Accepted", client_info)

try :
    while True :
        data = client_socket.recv(1024)
        if len(data) == 0: break
        print("received [%s] " % data)
except IOError :
    pass

print("disconnected")

client_socket.close()
server_sock.close()
print("bye")