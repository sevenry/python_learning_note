import urllib.request

def get_price():
    page= urllib.request.urlopen("https://www.taobao.com")
    text=page.read().decode("utf8")
    where=text.find('Fact%2F')
    start=where+7
    end=where+9
    return(float(text[start:end]))
    
price=get_price()

   
