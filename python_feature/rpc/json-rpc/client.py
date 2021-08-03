import socket
import json


class TCPClient(object):
    """
    负责网络连接
    """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def recv(self, length):
        return self.sock.recv(length)

    def send(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.close()


class _Method(object):
    """
    负责方法调用
    """
    def __getattr__(self, method):

        def func(*args, **kwargs):
            info = {
                'name': method,
                'args': args,
                'kwargs': kwargs
            }
            self.send(json.dumps(info).encode('utf-8'))
            data = self.recv(1024)
            return json.loads(data)['result']

        setattr(self, method, func)
        return func


class ServerProxy(TCPClient, _Method):

    def __init__(self, host='127.0.0.1', port=1060):
        TCPClient.__init__(self)
        self.connect(host, port)


if __name__ == '__main__':
    cli = ServerProxy('127.0.0.1', 1061)
    # ret = cli.add(1, 2, c = 4)
    # print(f"return of add is: {ret}")
    ret = cli.minus(1, 2)
    print(f"return of minus is: {ret}")
