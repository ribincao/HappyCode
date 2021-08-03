from functools import partial
class TCPServer:
    pass


class RPCDispath:
    
    def __init__(self):
        self.methods = {}
        self.instance = None

    def register_function(self, function=None, name=None):
        if function is None:
            return partial(self.register_function, name=name)
        if name is None:
            name = function.__name__
        
        self.methods[name] = function
        return function
    
    def _dispatch(self, method, params):
        try:
            func = self.methods[method]
        except KeyError:
            pass
        else:
            if func is not None:
                return func(*params)
            raise Exception(f"method '{method}' is not supported")
        


class Server(TCPServer, RPCDispath):

    def __init__(self, addr):
        RPCDispath.__init__(self)
        TCPServer.__init__(self, addr)


def respon_string(s):
    return f"get string: {s}"

if __name__ == '__main__':
    srv = Server(('localhost', 1060))
    _ = srv.register_function(respon_string, "get_string")
    print(f"listen as {1060}")
    srv.serve_forever()