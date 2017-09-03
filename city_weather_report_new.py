import time
from bs4 import BeautifulSoup
import re
import requests

header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"}

weather_homepage = "http://www.weather.com.cn/static/html/weather_list.shtml"

#-------------------------------

def get_html(url):   # 获取目标网址的html
    try:
        time.sleep(3)
        response = requests.get(url,headers=header)
        response.encoding ='utf-8'
        html = response.text
        #print(html)
        return html  
    except requests.RequestException as e:
        print(e)

#-------------------------------

def bs_url(html):  #对html进行解析，返回soup

    soup = BeautifulSoup(html,'lxml')
    # 这里采用的lxml HTML 解析器
    # BeautifulSoup(html, "html.parser") 则是Python标准解析器
    return soup

#-------------------------------
def insert(originalList, new, pos): 
#Inserts new inside original at pos.
    return originalList[:pos] + new + originalList[pos:]
#-------------------------------

def get_pages_list(soup):   # 返回的是所有城市及天气网址的列表，元组
    
    global city_url_dict
    city_url_dict={}
    city_url_list=[]

    for province in soup.find_all(class_="tmapin_citylist"):
        print("\n【"+province.p.string+"】")
        for each_city in province.ul.find_all('li'):
            original_city_href = each_city.a['href']  #原始的这个网址是 一周天气网页，要改成当天的
            city_href = insert(original_city_href, "1d", 33)
            
            city_url_dict[each_city.string] = city_href  #把'城市名':'网址' 存入词典中
            
            each_dict={}
            each_dict[each_city.string] = city_href
            city_url_list.append(each_dict)   # 把{'城市名':'网址'} 存入列表中

            print("%s \t"%(each_city.string), end ="")        
 
    #print(city_url_list)
    #return city_url_dict
    return city_url_list,city_url_dict
            
#-------------------------------

def get_weather_info_list(url):   # 返回天气信息的列表形式。。这只是个中间函数

    soup = bs_url(get_html(url))

    weather_info_list = []        

    for each in soup.find_all("h1"):    #for tag in soup.find_all(re.compile("^b")):

        if(re.search((r'^\d?\d?日白天|^\d?\d?日夜间'),str(each.string))):  # 千万注意啊，这里的 i.string 不是字符型
            #print(each)
            #print(each.parent)
            #print(each.next_sibling)                    # 千万注意啊，下一个兄弟节点，往往是 换行符！！！
            #print(each.next_sibling.next_sibling)       # 所以在下面，我干脆用了父节点。
            li = each.parent
            if(li.div!=None):    # 中国天气网，不同地区的网页的 天气一栏的 HTML 格式有所区别，有的有一个不显示的div节点
                li.div.clear()   # 这个方法很有用，删除 li.div节点的sting         
            
            for string in li.stripped_strings:   # 把非字符的都去掉   
                #print(string)
                weather_info_list.append(string)

    #print(weather_info_list)
    return weather_info_list

#-------------------------------

def get_weather_dict(city_dict):   # 输入 {城市:网址} 词典，输出 天气信息词典

    city_name = [key for key,value in city_dict.items()][0]   # 自己很满意的提取字典键值对的写法。
    #print(city_name)
    city_url =  [value for key,value in city_dict.items()][0]    
    #print(city_url)

    weather_info_List = get_weather_info_list(city_url)    
                
    weather_dict = {}
    weather_dict['城市'] = city_name
    weather_dict['时间1'] = weather_info_List[0]
    weather_dict['天气1'] = weather_info_List[1]
    weather_dict['气温1'] = weather_info_List[2]+"℃"
    weather_dict['风级1'] = weather_info_List[4]
    weather_dict['日落/日升时刻1'] = weather_info_List[5]
    weather_dict['时间2'] = weather_info_List[6]
    weather_dict['天气2'] = weather_info_List[7]
    weather_dict['气温2'] = weather_info_List[8]+"℃"
    weather_dict['风级2'] = weather_info_List[10]
    weather_dict['日落/日升时刻2'] = weather_info_List[11]   

    return weather_dict

#-------------------------------

def print_city_weather(city_dict):  # 把天气字典数据，格式化打印输出

    weather_dict = get_weather_dict(city_dict)
    
    print("==============================")
    print('     城市天气预报（'+weather_dict['城市']+'）    ')
    print('------------------------------')
    print('时间:'+weather_dict['时间1']) 
    print('天气:'+weather_dict['天气1'])  
    print('气温:'+weather_dict['气温1'])  
    print('风级:'+weather_dict['风级1']) 
    print('Time:'+weather_dict['日落/日升时刻1'])
    print('------------------------------')
    print('时间:'+weather_dict['时间2']) 
    print('天气:'+weather_dict['天气2'])  
    print('气温:'+weather_dict['气温2'])  
    print('风级:'+weather_dict['风级2']) 
    print('Time:'+weather_dict['日落/日升时刻2'])    
    print('------------------------------')
    print('(现在时刻：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+')')
    print("==============================")

#-------------------------------

def run(maxnum):  #循环maxnum次，按顺序输出各大城市的天气

    city_url_list = get_pages_list(bs_url(get_html(weather_homepage)))[0]  # 返回 储存单元词典的列表,加[0]的原因是，函数返回一个列表和一个词典，取前者

    #dict1={'香港':"http://www.weather.com.cn/weather1d/101320101.shtml"}
       
    time.sleep(2)

    num=0

    for each_dict in city_url_list:
        time.sleep(2)
  
        print(each_dict)
        try:
            print_city_weather(each_dict)
        except:
            print("该城市天气获取失败！")

        num += 1
        if(num>maxnum):
            break
        else:
            print("第"+str(num)+"次循环。\n")           

#-------------------------------

def run_test():

    url_dict={}
    
    cities_dict = get_pages_list(bs_url(get_html(weather_homepage)))[1]  #{'城市'：'网址',......}
    cities=[key for key in cities_dict]   #把词典中的城市都存到列表中
    #print('\n以上为可查询的所有城市。')
    #print(cities)
    print("\n··························································")
        
    Flag="y"
    while (Flag != ('n' and 'N')):
        cityname = input("请输入您所要查询的城市名称：")
        city_dict={}
        if (cityname in cities):   #若找到这个城市
            cityurl = cities_dict[cityname]     # 找到对应的网址
            city_dict[cityname] = cityurl       # 形成一个小词典
            print(city_dict)
        
            try:
                print_city_weather(city_dict)
            except requests.HTTPError as e:
                print("该城市天气获取失败！")
                print(e.message)
        
        else:
            print("未找到该城市.")

        Flag=input("还想要继续查询吗？(y/n):")
    

#-------------试运行---------------
if __name__ == '__main__':

    #run(15)
    run_test()

    
    
    








            
        
