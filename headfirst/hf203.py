import urllib.request
page= urllib.request.urlopen("https://www.taobao.com")
text=page.read().decode("utf8")
where=text.find('yegai')

start=where+2
end=where+5

ak=text[start:end]
akk=ak.lower()
print(akk)
