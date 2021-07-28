import requests


# 构造 url 获取查询响应
def geocode(address):
    paramters = {'address': address, 'output': 'json'}
    base = 'http://api.map.baidu.com/geocoder'
    response = requests.get(base, params=paramters)
    answer = response.json()
    print(answer['result'])


if __name__ == '__main__':
    geocode('景德镇市浮梁')
