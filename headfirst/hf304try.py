import urllib.request
import time

def set_password():
    password=input("imput your password")
    return(password)

password=set_password()

def send_to_mail(msg):
    password_manager=urllib.request.HTTPPasswordMgr()
    password_manager.add_password("mail","http://mail.qq.com","835266995@qq.com",password)
    http_handler=urllib.request.HTTPBasicAuthHandler(password_manager)
    page_opener=urllib.request.build_opener(http_handler)
    urllib.request.install_opener(page_opener)
    params=urllib.parse.urlencode({'status':msg}).encode(encoding='UTF8')
    resp=urllib.request.urlopen("http://mail.qq.com/update.json",params)
    resp.read()

def get_price():
    page= urllib.request.urlopen("https://www.taobao.com")
    text=page.read().decode("utf8")
    where=text.find('Fact%2F')
    start=where+7
    end=where+9
    return(float(text[start:end]))
price=get_price()

ans=input("do you want the answer instantly: ")
if ans=="y":
    print(price)
    send_to_mail(get_price())
else:
    price=99.9
    while price>20:
        time.sleep(10)
        price=get_price()
        
    print("buy")

   
