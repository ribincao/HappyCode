import http.client
import json
from urllib.parse import quote_plus


base = '/geocoder'


# 直接使用 http 协议
def geocode(address):
    path = f'{base}?address={quote_plus(address)}&output=json'
    connection = http.client.HTTPConnection('api.map.baidu.com')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    print(reply['result'])


if __name__ == '__main__':
    geocode('景德镇市浮梁')
