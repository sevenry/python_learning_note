from random import randint
secret=randint(1,10)
print("welcome")
g=input("guess the number: ")
guess=int(g)
while guess!=secret:
    if guess>secret:
        print("too high")
    else:
        print("too low")
    g=input("input again ")
    guess=int(g)
print("you win")
print("congratulation~~~i am so clever~~~")
