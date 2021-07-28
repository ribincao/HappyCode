import socket
from urllib.parse import quote_plus


request_txt = """\
GET /geocoder?address={}&output=json HTTP/1.1\r\n\
Host: api.map.baidu.com:80\r\n\
User-Agent: search4.py (Foundations of Python Network Programming)\r\n\
Connection: close\r\n\
\r\n
"""


# 建立会话
def geocode(address):
    sock = socket.socket()
    sock.connect(('api.map.baidu.com', 80))
    request = request_txt.format(quote_plus(address))
    sock.sendall(request.encode('ascii'))
    # 字节串以 b 开头
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))


if __name__ == '__main__':
    geocode('景德镇市浮梁')
