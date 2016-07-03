import urllib.request
import time
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
else:
    price=99.9
    while price>20:
        time.sleep(10)
        price=get_price()
        
    print("buy")

   
