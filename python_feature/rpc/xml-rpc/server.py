from xmlrpc.server import SimpleXMLRPCServer


def respon_string(s):
    return f"get string: {s}"


if __name__ == '__main__':
    srv = SimpleXMLRPCServer(('localhost', 1060))
    srv.register_function(respon_string, "get_string")
    print(f"listen at {1060}")
    srv.serve_forever()