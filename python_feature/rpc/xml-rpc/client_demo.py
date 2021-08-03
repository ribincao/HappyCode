import urllib


class ServerProxy:

    def __init__(self, uri):
        pass

    def _request(self, methodname, params):
        request = "xxx"
        response = self._transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
        )
        if len(response) == 1:
            response = response[0]
        return response

    def __getattr__(self, name):
        return _Method(self._request, name)


class _Method:

    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, f"{self.__name}.{name}")

    def __call__(self, *args):
        return self.__send(self.__name, args)


if __name__ == '__main':
    cli = ServerProxy("http://localhost:1060")
    ret = cli.get_string("hello")
    print(ret)
