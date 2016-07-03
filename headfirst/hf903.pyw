from tkinter import *
import pygame.mixer
from tkinter.messagebox import askokcancel# 换成 import tkinter.messagebox 需要写成
# tkinter.messagebox.askokcancel

def track_start():
    track.play(loops=-1)#loops=-1参数重复播放歌曲

def track_stop():
    track.stop()

def shutdown():
    if askokcancel(title='are u sure',message='do u really want to quit'):
        app.destroy()#为什么内容是‘’不是”“
    #track.stop()
    #app.destroy()
    
app=Tk()
app.title("head first mix")
app.geometry('250x100+200+100')

mixer=pygame.mixer
mixer.init()#启动声音系统

sound_file="correct.wav"#确定歌曲
#确定歌曲和启动声音系统先后不重要
track=mixer.Sound(sound_file)

#track_playing=IntVar() 书上327将这一行与 stop和destroy同时写入，但是不写这一行也可以运行呀
start_button=Button(app,command=track_start,text="start")
start_button.pack(side=LEFT)

stop_button=Button(app,command=track_stop,text="stop")
stop_button.pack(side=RIGHT)

app.protocol("WM_DELETE_WINDOW",shutdown)#应用程序窗口app的protocol()方法
#WM_DELETE_WINDOW是tkinter的属性，还有WM_TAKE_FOCUS,WM_SAVE_YOURSELF
#“WM_DELETE_WINDOW”是protocol()中的某个索引，对应着其中另外的操作
app.mainloop()

