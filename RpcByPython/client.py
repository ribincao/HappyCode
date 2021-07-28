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
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, f"{self.__name}.{name}")

    def __call__(self, *args, **kwargs):
        return self.__send(self.__name, args, kwargs)


class ServerProxy(TCPClient, _Method):

    def __init__(self, host='127.0.0.1', port=1060):
        TCPClient.__init__(self)
        self.connect(host, port)

    def __getattr__(self, name):
        return _Method(self._request, name)

    def _request(self, method_name, args, kwargs):
        info = {
            'name': method_name,
            'args': args,
            'kwargs': kwargs
        }
        self.send(json.dumps(info).encode('utf-8'))
        data = self.recv(1024)
        return json.loads(data)['result']


if __name__ == '__main__':
    cli = ServerProxy('127.0.0.1', 1061)

    ret = cli.ping()
    print(f"return of ping is: {ret}")
    ret = cli.add(1, 2)
    print(f"return of add(1, 2) is: {ret}")
    ret = cli.valid_method(1, 2)
    print(f"return of valid_method is: {ret}")

    # print(dir(cli))
