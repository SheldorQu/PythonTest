import urllib.request
import urllib.parse
# import urllib.request,不是 urillib
# 可以将url先构造成一个Request对象，传进urlopen       
# Request存在的意义是便于在请求的时候传入一些信息，而urlopen则不
# 在Python 3以后的版本中，urllib2这个模块已经不单独存在，
# urllib2被合并到了urllib中，叫做urllib.request 和 urllib.error。
# urllib整个模块分为urllib.request, urllib.parse, urllib.error。
# 例：
# urllib2.urlopen()变成了urllib.request.urlopen()
# urllib2.Request()变成了urllib.request.Request()
# 需要用urllib.parse来 urlencode 参数data

# 类 urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)

#------------------------------

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}

aim_url= "http://www.douban.com"

#------------------------------

data_header = urllib.parse.urlencode(header) # header需要先encode后，才能传入Request

req = urllib.request.Request(aim_url,data=None,headers=header) # Request类

try:
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    # 最好在后面加个 .decode('utf-8')
    print(html)
except urllib.request.URLError as e:
    print(e.reason)
