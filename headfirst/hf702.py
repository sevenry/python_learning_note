import pygame.mixer
sounds=pygame.mixer
sounds.init()

def wait_finish(channel):
    while channel.get_busy():#get_busy()检查声音是否在被播放
        pass#不做任何事情

correct_s=sounds.Sound("correct.wav")
wrong_s=sounds.Sound("wrong.wav")

prompt="1 is correct, 2 is wrong, 3 is over: "

asked_number=0
correct_number=0
wrong_number=0


choice=input(prompt)# 利用prompt作为替换
while choice!='3':
    asked_number=asked_number+1
    if choice=='1':
        correct_number=correct_number+1
        wait_finish(correct_s.play())
    else:
        wrong_number=wrong_number+1
        wait_finish(wrong_s.play())
    choice=input(prompt)

print("u have answered "+str(asked_number)+" questions")
print(str(correct_number)+" are right")
print(str(wrong_number)+" are wrong")
