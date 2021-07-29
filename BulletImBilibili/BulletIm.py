import requests
from pyquery import PyQuery as pq


def get_bullet_from_bilibili(oid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + oid
    div = 'd'  # find <d></d>
    get_bullet(url, div)


def get_bullet(url, div):
    headers = {'cookie': 'bsource=...'}  # header
    result = requests.get(url, headers=headers)
    result.encoding = 'utf-8'
    html = pq(result.content)
    bullets = html.find(div)
    output(bullets)


def output(bullets):
    cnt = 0
    ret = []
    conditions = ['2021', '北京']
    for bullet in bullets:
        ret.append(bullet.text)
        for condition in conditions:
            if condition in bullet.text:
                cnt += 1
    # print(ret)
    print(f"Num of all bullets: {len(bullets)}")
    print(f"Num of bullets contain {conditions}: {cnt}")
    print(str(round(cnt / len(bullets), 3)) + '%')

if __name__ == '__main__':
    get_bullet_from_bilibili('373384747')
