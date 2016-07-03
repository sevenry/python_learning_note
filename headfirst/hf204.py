import urllib.request
import time
price=99.9
aa=time.clock()
print("time.daylight canno be used ")
cc=time.time()
print(cc)
while price>10:
    time.sleep(100)
    page= urllib.request.urlopen("https://www.taobao.com")
    text=page.read().decode("utf8")
    where=text.find('Fact%2F')
    start=where+7
    end=where+9
    price=float(text[start:end])
    print(price)
print("buy")
