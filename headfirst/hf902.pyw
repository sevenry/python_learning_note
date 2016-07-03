from tkinter import *
import pygame.mixer

def track_start():
    track.play(loops=-1)#loops=-1参数重复播放歌曲

def track_stop():
    track.stop()

def shutdown():
    track.stop()
    
app=Tk()
app.title("head first mix")
app.geometry('250x100+200+100')

mixer=pygame.mixer
mixer.init()#启动声音系统

sound_file="correct.wav"#确定歌曲
#确定歌曲和启动声音系统先后不重要
track=mixer.Sound(sound_file)

start_button=Button(app,command=track_start,text="start")
start_button.pack(side=LEFT)

stop_button=Button(app,command=track_stop,text="stop")
stop_button.pack(side=RIGHT)

app.protocol("WM_DELETE_WINDOW",shutdown)#应用程序窗口app的protocol()方法

app.mainloop()

