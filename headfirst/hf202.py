import urllib.request
page= urllib.request.urlopen("https://www.taobao.com")
text=page.read().decode("utf8")
where=text.find('>$')

start=where+1
end=where+15

ak=text[start:end]
print(ak)
