from hf6transactions import *
import hf6promotion 
import hf6starbuzz 

items=["donut","latte","filter","muffin"]
prices=[1.50,2.0,1.80,1.20]
running=True

while running:
    option=1
    for choice in items:
        print(str(option)+". "+choice)
        option=option+1
    print(str(option)+". quit")
    choice=int(input("choose an option: "))
    if choice==option:
        running=False
    else:
        credit_card=input("credit card number: ")
        price=hf6promotion.discount(prices[choice-1])
        g=input("do you have a id card?y/n: ")
        if g=="y":
            price=hf6starbuzz.discount(price)
        save_transaction(price,credit_card,items[choice-1])
