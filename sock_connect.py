import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = socket.gethostbyname('frpi.ddns.net')
port = 80

message = "GET / HTTP/1.1\r\nHost: frpi.hopto.org\r\n\r\n"

s.connect((ip, port))
s.send(message.encode())

info = s.recv(2048)

print(info.decode('utf-8'))