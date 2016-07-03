import urllib.request
page= urllib.request.urlopen("https://www.taobao.com")
text=page.read().decode("utf8")

print(text)
