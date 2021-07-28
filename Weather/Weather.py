import requests
import json
from bs4 import BeautifulSoup
import csv


class Weather:

    def __init__(self, code: str, name: str):
        self._url = 'http://www.weather.com.cn/weather/' + code + '.shtml'
        self._text = ""
        self.data_all = []
        self.city_name = name
        self.data_cur = None
        self.data_7 = None

    def run(self):
        self.get_html_text()
        self.get_content()
        self.write_to_csv(14)

    def get_html_text(self):
        """请求获得网页内容"""
        resp = ""
        try:
            resp = requests.get(self._url, timeout=30)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            print(f"{self.city_name} Success")
            self._text = resp.text
        except requests.HTTPError as e:
            print(e)
            print(f"status_code {resp.status_code}")
        except Exception as oe:
            print(oe)

    def get_content(self):
        """处理得到有用信息保存数据文件"""
        final = []  							      # 初始化一个列表保存数据
        bs = BeautifulSoup(self._text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body
        data = body.find('div', {'id': '7d'})         # 找到div标签且id = 7d
        # 下面爬取当天的数据
        data2 = body.find_all('div', {'class': 'left-div'})
        text = data2[2].find('script').string
        text = text[text.index('=') + 1:-2]		 # 移除改var data=将其变为json数据
        jd = json.loads(text)
        day_one = jd['od']['od2']				 # 找到当天的数据
        final_day = []						     # 存放当天的数据
        count = 0
        for i in day_one:
            temp = []
            if count <= 23:
                temp.append(i['od21'])				 # 添加时间
                temp.append(self.city_name + '市')	 # 添加城市
                temp.append(i['od22'])				 # 添加当前时刻温度
                temp.append(i['od24'])				 # 添加当前时刻风力方向
                temp.append(i['od25'])				 # 添加当前时刻风级
                temp.append(i['od26'])				 # 添加当前时刻降水量
                temp.append(i['od27'])				 # 添加当前时刻相对湿度
                temp.append(i['od28'])				 # 添加当前时刻控制质量
                final_day.append(temp)
                self.data_all.append(temp)
            count = count + 1
        # 爬取 24h 的数据
        ul = data.find('ul')                     # 找到所有的 ul 标签
        li = ul.find_all('li')                   # 找到左右的 li 标签
        i = 0                                    # 控制爬取的天数
        for day in li:                           # 遍历找到的每一个 li
            if 7 > i > 0:
                temp = []                        # 临时存放每天的数据
                date = day.find('h1').string     # 得到日期
                date = date[0:date.index('日')]  # 取出日期号
                temp.append(date)
                inf = day.find_all('p')          # 找出 li 下面的 p 标签,提取第一个p标签的值, 即天气
                temp.append(inf[0].string)

                tem_low = inf[1].find('i').string  	# 找到最低气温

                if inf[1].find('span') is None:  	# 天气预报可能没有最高气温
                    tem_high = None
                else:
                    tem_high = inf[1].find('span').string  # 找到最高气温
                temp.append(tem_low[:-1])
                if tem_high[-1] == '℃':
                    temp.append(tem_high[:-1])
                else:
                    temp.append(tem_high)

                wind = inf[2].find_all('span')		# 找到风向
                for j in wind:
                    temp.append(j['title'])

                wind_scale = inf[2].find('i').string # 找到风级
                index1 = wind_scale.index('级')
                temp.append(int(wind_scale[index1-1:index1]))
                final.append(temp)
            i = i + 1
        self.data_cur = final_day
        self.data_7 = final

    def write_to_csv(self, day):
        """保存为csv文件"""
        file_name = self.city_name + ".csv"
        with open(file_name, 'w', errors='ignore', newline='') as f:
            if day == 14:
                header = ['日期', '城市', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
            else:
                header = ['小时', '城市', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(self.data_all)


if __name__ == '__main__':
    city_dict = {"南昌": "101240101",
                 "九江": "101240201",
                 "上饶": "101240301",
                 "抚州": "101240401",
                 "宜春": "101240501",
                 "吉安": "101240601",
                 "赣州": "101240701",
                 "景德镇": "101240801",
                 "萍乡": "101240901",
                 "新余": "101241001",
                 "鹰潭": "101241101", }
    for city_name, city_code in city_dict.items():
        if city_name == "景德镇":
            w = Weather(city_code, city_name)
            w.run()

