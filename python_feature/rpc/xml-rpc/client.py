from xmlrpc.client import ServerProxy


if __name__ == '__main__':
    cli = ServerProxy("http://localhost:1060")
    ret = cli.get_string("hello")
    print(ret)