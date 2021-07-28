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
        (conn, _) = self.sock.accept()
        self.conn = conn

    def recv(self):
        msg = self.conn.recv(1024)
        return msg

    def send(self, data):
        self.conn.sendall(data)

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

    def call_method(self, data):
        self.data = json.loads(data.decode('utf-8'))
        name = self.data['name']
        args = self.data['args']
        kwargs = self.data['kwargs']
        if name not in self.methods:
            data = {
                "result": f"there is no support for {name}."
            }
        else:
            ret = self.methods[name](*args, **kwargs)
            data = {
                "result": ret
            }
        ret = json.dumps(data).encode('utf-8')
        return ret


class Server(TCPServer, Dispatch):

    def __init__(self):
        TCPServer.__init__(self)
        Dispatch.__init__(self)

    def run(self, port):
        print(f"Server listen at {port}.")
        self.listen(port)
        print("get connection")
        while True:
            data = self.recv()
            if data:
                ret = self.process(data)
                self.send(ret)

    def process(self, msg):
        return self.call_method(msg)


#  测试方法
def ping():
    return "pong"


class Test:

    @staticmethod
    def add(a, b):
        return a + b


if __name__ == "__main__":
    srv = Server()
    srv.register_method(ping)
    srv.register_method(Test.add)
    srv.run(1061)
