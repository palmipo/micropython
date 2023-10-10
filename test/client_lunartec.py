import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.229', 2222))
time.sleep(5)
sock.send("Hello World !!!".encode())
sock.send("quit".encode())
time.sleep(5)
sock.close()
