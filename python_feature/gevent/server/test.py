from gevent.monkey import patch_all
from gevent.server import StreamServer
patch_all()


def main(sock, addr):
    sock.recv(4096)
    sock.send("HTTP/1.1 200 OK\n\n<h1>Hello World!</h1>")


if __name__ == '__main__':
    s = StreamServer(("127.0.0.1", 1060), main)
    s.serve_forever()
