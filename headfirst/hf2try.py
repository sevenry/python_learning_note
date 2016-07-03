import urllib.parse
import urllib.request
url = 'http://www.baidu.com/s'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'WHY',    
         'location' : 'SDU',    
         'language' : 'Python',
         'ie' : 'utf-8',
         'wd' : 'python' }
headers = { 'User-Agent' : user_agent }
data = urllib.parse.urlencode(values)
#data=data.encode(encoding='UTF8')
req = urllib.request.Request(url+'?'+data)
#, data, headers)
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page.decode('UTF8'))
