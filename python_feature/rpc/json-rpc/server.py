import json
import socket


class TCPServer(object):
    """
    负责网络连接
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def listen(self, port):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(5)

    def recv(self):
        (conn, _) = self.sock.accept()
        msg = conn.recv(1024)
        self.conn = conn
        return msg

    def send(self, data):
        self.conn.sendall(data)
        self.close()

    def close(self):
        self.conn.close()


class Dispatch(object):
    """
    负责方法注册和调用
    """
    def __init__(self):
        self.methods = {}
        self.data = None

    def register_method(self, method, name=None):
        if not name:
            name = method.__name__
        self.methods[name] = method

    def loads(self, data):
        self.data = json.loads(data.decode('utf-8'))

    def call_method(self, data):
        self.loads(data)
        name = self.data['name']
        args = self.data['args']
        kwargs = self.data['kwargs']
        ret = self.methods[name](*args, **kwargs)
        data = {
            "result": ret
        }
        return json.dumps(data).encode('utf-8')


class Server(TCPServer, Dispatch):

    def __init__(self):
        TCPServer.__init__(self)
        Dispatch.__init__(self)

    def loop(self, port):
        self.listen(port)
        print(f"Server listen at {port}.")
        while True:
            data = self.recv()
            if data:
                ret = self.process(data)
                self.send(ret)

    def process(self, msg):
        return self.call_method(msg)


#  测试方法
def add(a, b, c=10):
    return a + b + c


class Test:

    @staticmethod
    def minus(a, b):
        return a - b


if __name__ == "__main__":
    srv = Server()
    srv.register_method(add)
    srv.register_method(Test.minus)
    srv.loop(1061)
