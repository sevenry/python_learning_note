from hf6transactions import *
from hf6promotion import *
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
        new_price=discount(prices[choice-1])
        save_transaction(new_price,credit_card,items[choice-1])
