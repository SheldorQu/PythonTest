#================================================================================
#                        从人民网博客中下载文章                                  #        
#================================================================================
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import time
# import urllib.request,不是 urillib
# 可以将url先构造成一个Request对象，传进urlopen       
# Request存在的意义是便于在请求的时候传入一些信息，而urlopen则无
# 在Python 3以后的版本中，urllib2这个模块已经不单独存在，
# urllib2被合并到了urllib中，叫做urllib.request 和 urllib.error。
# urllib整个模块分为urllib.request, urllib.parse, urllib.error。
# 
# urllib2.urlopen()变成了urllib.request.urlopen()
# urllib2.Request()变成了urllib.request.Request()
# 需要用urllib.parse来 urlencode 参数data
# 类 urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)

#------------------------------

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/35.0.1916.153 Safari/537.36'}


aim_url_start = "http://blog.people.com.cn/article/1501031758615.html"  # 爬取的初始网页


#------------------------------

def get_html(aim_url):  # 返回目标url的爬取代码
    
    data_header = urllib.parse.urlencode(header) # header需要先encode后，才能传入Request

    req = urllib.request.Request(aim_url,data=None,headers=header) # Request类

    try:
        time.sleep(2)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        # 最好在后面加个 .decode('utf-8')
        #print(html)
        return html
    except urllib.request.ULRError as e:
        print(e.reason)
 
#-------------------------------

def bs_url(html):  #对html进行解析，返回soup

    soup = BeautifulSoup(html,'lxml')
    # 这里采用的lxml HTML 解析器
    # BeautifulSoup(html, "html.parser") 则是Python标准解析器
    return soup

#-------------------------------

def get_article_list(soup):   # 返回的是 文章的各段落组成的列表
    
    list_article=[]

    for string_header in soup.find_all('strong'):
        if(len(string_header.string)>=14):
            print("文章题目： "+ repr(string_header.string))
            list_article.append(string_header.string)  # 存储标题
            break
    
    for string_each in soup.find_all('span'):  # span标签的集合
        for sub_string in string_each.strings:
        #用了两层循环：因为某些span模块中，含有多个节点，直接用.string,将返回None        
            #print(repr(sub_string))            
            list_article.append(sub_string)

    return list_article
        
#-------------------------------
        
def write_article(art_List,name):  # 保存文章
    
    with open(name+'.txt','a',encoding='utf-8') as f:   # 这里多加了一个encoding='utf-8'，防止win下的编码GBK问题
        for para in art_List:
            if (para[-1]==']' or para[-1]=='|'):
                para=""
                f.write(para)
            else:
                f.write(para+'\n    ')

    print("文章 "+name+" 保存完成! ")


#-------------------------------

def get_go_ahead_page(soup):    # 获取该页面的“上一页”和“下一页”链接网址

    go_ahead_page_dic = {}  

    for string_last_page in soup.find_all('em'):
        if(len(string_last_page.a.string)>10):
            last_page = "http://blog.people.com.cn"+string_last_page.a['href']
            # 提取出了该网页末尾“上一篇”所指向的网址
            print("本篇文章的上一篇链接： " + last_page)
            go_ahead_page_dic['last_page'] = last_page # 将上一篇的网址保存到词典中
            

    for string_next_page in soup.find_all('i'):
        if(len(string_next_page)>1):                # 此处于上面不一样。        
            # 提取出了该网页末尾“下一篇”所指向的网址            
            if('http' not in string_next_page.a['href']):   #判断出来有两个 href                
                next_page = "http://blog.people.com.cn" + string_next_page.a['href']
                #print("本篇文章的下一篇链接： "+ next_page)
                go_ahead_page_dic['next_page'] = next_page   # 将下一篇的网址保存到词典中
           
    
    return last_page  #先只返回上一页

    #return go_ahead_page_dic    #通过dict，可以实现向前翻页爬取，或者向后翻页爬取


#-------------------------------


def run(url,num):   # 迭代运行，num为迭代次数

    write_article(get_article_list(bs_url(get_html(url))),'article'+str(num))
    
    next_url = get_go_ahead_page(bs_url(get_html(url)))

    if(num>0):
        run(next_url,num-1)
    
  

#--------------试运行-------------

if __name__ == '__main__':

    run(aim_url_start,6)  #迭代6次，爬取七个网页博客，并保存本地程序文件夹



    

    
    


