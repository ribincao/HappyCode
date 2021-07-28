import requests
import json
from bs4 import BeautifulSoup
import csv
import numpy as np
import matplotlib as plt
import math
data_all = []


def get_html_text(url):
    """请求获得网页内容"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("Success")
        return r.text
    except Exception as e:
        print(e)
        return " "


def get_content(html, cityname):
    """处理得到有用信息保存数据文件"""
    final = []  							 # 初始化一个列表保存数据
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    data = body.find('div', {'id': '7d'})    # 找到div标签且id = 7d
    # 下面爬取当天的数据
    data2 = body.find_all('div',{'class':'left-div'})
    text = data2[2].find('script').string
    text = text[text.index('=')+1 :-2]		 # 移除改var data=将其变为json数据
    jd = json.loads(text)
    dayone = jd['od']['od2']				 # 找到当天的数据
    final_day = []						     # 存放当天的数据
    count = 0
    for i in dayone:
        temp = []
        if count <=23:
            temp.append(i['od21'])				 # 添加时间
            temp.append(cityname+'市')			# 添加城市
            temp.append(i['od22'])				 # 添加当前时刻温度
            temp.append(i['od24'])				 # 添加当前时刻风力方向
            temp.append(i['od25'])				 # 添加当前时刻风级
            temp.append(i['od26'])				 # 添加当前时刻降水量
            temp.append(i['od27'])				 # 添加当前时刻相对湿度
            temp.append(i['od28'])				 # 添加当前时刻控制质量
            # 			print(temp)
            final_day.append(temp)
            data_all.append(temp)
        count = count +1
    # 下面爬取24h的数据
    ul = data.find('ul')                     # 找到所有的ul标签
    li = ul.find_all('li')                   # 找到左右的li标签
    i = 0                                    # 控制爬取的天数
    for day in li:                          # 遍历找到的每一个li
        if i < 7 and i > 0:
            temp = []                        # 临时存放每天的数据
            date = day.find('h1').string     # 得到日期
            date = date[0:date.index('日')]  # 取出日期号
            temp.append(date)
            inf = day.find_all('p')          # 找出li下面的p标签,提取第一个p标签的值，即天气
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
    return final_day, final


def write_to_csv(file_name, data, day=14):
    """保存为csv文件"""
    with open(file_name, 'a', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期','城市','天气','最低气温','最高气温','风向1','风向2','风级']
        else:
            header = ['小时','城市','温度','风力方向','风级','降水量','相对湿度','空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)


def wind_radar(data):
    """风向雷达图"""
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])
    for i in range(0,24):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315
    degs = np.arange(45,361,45)
    temp = []
    for deg in degs:
        speed = []
        # 获取 wind_deg 在指定范围的风速平均值数据
        for i in range(0,24):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed)/len(speed))
    print(temp)
    N = 8
    theta = np.arange(0.+np.pi/8,2*np.pi+np.pi/8,2*np.pi/8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1-x/max(temp), 1-x/max(temp),0.6) for x in radii]
    plt.bar(theta,radii,width=(2*np.pi/N),bottom=0.0,color=colors)
    plt.title('河南风级图--Dragon少年',x=0.2,fontsize=16)
    plt.show()


def calc_corr(a, b):
    """计算相关系数"""
    a_avg = sum(a)/len(a)
    b_avg = sum(b)/len(b)
    cov_ab = sum([(x - a_avg)*(y - b_avg) for x,y in zip(a, b)])
    sq = math.sqrt(sum([(x - a_avg)**2 for x in a])*sum([(x - b_avg)**2 for x in b]))
    corr_factor = cov_ab/sq
    return corr_factor


def corr_tem_hum(data):
    """温湿度相关性分析"""
    tem = data['温度']
    hum = data['相对湿度']
    plt.scatter(tem,hum,color='blue')
    plt.title("温湿度相关性分析图--Dragon少年")
    plt.xlabel("温度/℃")
    plt.ylabel("相对湿度/%")
    # plt.text(20,40,"相关系数为："+str(calc_corr(tem,hum)),fontdict={'size':'10','color':'red'})
    plt.show()
    print("相关系数为："+str(calc_corr(tem,hum)))


from pyecharts import options as opts
from pyecharts.charts import Map,Timeline
#  定义一个timeline和map的组合图
def timeline_map(data):
    tl = Timeline().add_schema(play_interval =300,height=40,is_rewind_play=False,orient = "horizontal",is_loop_play = True,is_auto_play=False)#设置播放速度、是否循环播放等参数
    for h in time_line_final:
        x =data[data["小时"]==h]['城市'].values.tolist() #选取指定城市
        y=data[data["小时"]==h]['降水量'].values.tolist() #选取时间的降水量
        map_shape = (
            Map()
            .add("{}h时降水量（mm）".format(h),[list(z) for z in zip(x, y)],"河南") #打包输入地区及对应降水量数据
            .set_series_opts(label_opts=opts.LabelOpts("{b}")) #配置系列参数，{b}为显示地区数据
            .set_global_opts(
                title_opts=opts.TitleOpts(title="河南省降雨分布--Dragon少年"), #全局参数中设置标题
                visualmap_opts=opts.VisualMapOpts(max_=300,  #设置映射配置项的最大值
                                                  is_piecewise=True, #设置是否为分段显示
                                                  pos_top = "60%", #映射配置项距图片上部的距离
                                                  pieces=[
                                                        {"min": 101, "label": '>100ml', "color": "#FF0000"},  # 分段指定颜色及名称
                                                        {"min": 11, "max": 50, "label": '11-50ml', "color": "#FF3333"},
                                                        {"min": 6, "max": 10, "label": '6-10ml', "color": "#FF9999"},
                                                        {"min": 0.1, "max": 5, "label": '0.1-5ml', "color": "#FFCCCC"}])
        ))
        tl.add(map_shape, "{}h".format(h)) #将不同日期的数据加入到timeline中
    return tl



#  定义一个timeline和map的组合图
time_line_final = list(data1['小时'].iloc[0:24])
def timeline_map(data1):
    tl = Timeline().add_schema(play_interval =200,height=40,is_rewind_play=False,orient = "horizontal",is_loop_play = True,is_auto_play=True)#设置播放速度、是否循环播放等参数
    for h in time_line_final:
        x =data1[data1["小时"]==h]['城市'].values.tolist() #选取指定城市
        y=data1[data1["小时"]==h]['降水量'].values.tolist() #选取时间的降水量
        map_shape1 = (
            Map()
            .add("{}h时累计降水量（mm）".format(h),[list(z) for z in zip(x, y)],"河南") #打包输入地区及对应降水量数据
            .set_series_opts(label_opts=opts.LabelOpts("{b}")) #配置系列参数，{b}为显示地区数据
            .set_global_opts(
                title_opts=opts.TitleOpts(title="河南省累计降雨分布--Dragon少年"), #全局参数中设置标题
                visualmap_opts=opts.VisualMapOpts(max_=300,  #设置映射配置项的最大值
                                                  is_piecewise=True, #设置是否为分段显示
                                                  pos_top = "60%", #映射配置项距图片上部的距离
                                                  pieces=[
                                                        {"min": 251, "label": '特大暴雨', "color": "#800000"},  # 分段指定颜色及名称
                                                        {"min": 101, "max": 250, "label": '暴雨', "color": "#FF4500"},
                                                        {"min": 51, "max": 100, "label": '暴雨', "color": "#FF7F50"},
                                                        {"min": 25, "max": 50, "label": '大雨', "color": "#FFFF00"},
                                                        {"min": 10, "max": 25, "label": '中雨', "color": "#1E90FF"},
                                                        {"min": 0.1, "max": 9.9, "label": '小雨', "color": "#87CEFA"}])
        ))
        tl.add(map_shape1, "{}h".format(h)) #将不同日期的数据加入到timeline中
    return tl


if __name__ == '__main__':
    Citycode = {"郑州": "101180101",
                "新乡": "101180301",
                "许昌": "101180401",
                "平顶山": "101180501",
                "信阳": "101180601",
                "南阳": "101180701",
                "开封": "101180801",
                "洛阳": "101180901",
                "商丘": "101181001",
                "焦作": "101181101",
                "鹤壁": "101181201",
                "濮阳": "101181301",
                "周口": "101181401",
                "漯河": "101181501",
                "驻马店": "101181601",
                "三门峡": "101181701",
                "济源": "101181801",
                "安阳": "101180201"}
    citycode_lists = list(Citycode.items())
    for city_code in citycode_lists:
        city_code = list(city_code)
        print(city_code)
        citycode = city_code[1]
        cityname = city_code[0]
        url1 = 'http://www.weather.com.cn/weather/' + citycode + '.shtml'  # 24h天气中国天气网
        html1 = get_html_text(url1)
        data1, data1_7 = get_content(html1, cityname)  # 获得1-7天和当天的数据
write_to_csv('河南天气.csv', data_all, 1)
# timeline_map(data).render("rainfall.html")
timeline_map(data1).render("rainfalltoall_1.html")
