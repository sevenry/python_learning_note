import urllib.request
req=urllib.request.Request("http://beans-r-us.biz/prices.html")
page= urllib.request.urlopen(req)
text=page.read().decode("utf8")
print(text)
