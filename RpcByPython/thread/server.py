import json
import socket
import gevent
from threading import Thread


class TCPServer(object):
    """
    负责网络连接
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, port):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(5)

    @staticmethod
    def recv(conn):
        msg = conn.recv(1024)
        return msg

    @staticmethod
    def send(conn, data):
        conn.sendall(data)

    @staticmethod
    def close(conn):
        conn.close()


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
        while True:
            (conn, address) = self.sock.accept()
            print(f"{address} connected.")
            t = Thread(target=self.process, args=(conn, ))
            t.start()

    def process(self, conn):
        try:
            while True:
                msg = self.recv(conn)
                if not msg:
                    conn.shutdown(socket.SHUT_WR)
                else:
                    ret = self.call_method(msg)
                    self.send(conn, ret)
        except Exception as e:
            print(e)
        finally:
            self.close(conn)


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
