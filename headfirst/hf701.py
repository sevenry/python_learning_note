import pygame.mixer
sounds=pygame.mixer
sounds.init()

def wait_finish(channel):
    while channel.get_busy():
        pass

#s=sounds.Sound("correct.wav")
#wait_finish(s.play())#wait_finish 确保当前声音播放完再播放下一个
#s2=sounds.Sound("wrong.wav")
#wait_finish(s2.play())
s3=sounds.Sound("why.wav")
wait_finish(s3.play())
#s4=sounds.Sound("carhor.wav")
#wait_finish(s4.play())
