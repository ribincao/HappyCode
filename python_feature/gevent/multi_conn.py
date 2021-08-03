import socket
import threading
"""
模拟并发连接
"""

def sock_conn():
    client = socket.socket()

    client.connect(("localhost", 8001))
    count = 0
    while True:
        # msg = input(">>:").strip()
        # if len(msg) == 0:continue
        client.send(("hello %s" % count).encode("utf-8"))

        data = client.recv(1024)

        print("[%s]recv from server:" % threading.get_ident(), data.decode())  # 结果
        count += 1


for i in range(100):
    t = threading.Thread(target=sock_conn)
    t.start()
