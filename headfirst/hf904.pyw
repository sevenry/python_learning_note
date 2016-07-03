from tkinter import *
import pygame.mixer

def track_toggle():
    if track_playing.get()==1:
        track.play(loops=-1)
    else:
        track.stop()

def shutdown():
    track.stop()
    app.destroy()
    
app=Tk()
app.title("head first mix")
app.geometry('250x100+200+100')

mixer=pygame.mixer
mixer.init()#启动声音系统

sound_file="correct.wav"#确定歌曲
#确定歌曲和启动声音系统先后不重要
track=mixer.Sound(sound_file)

track_playing=IntVar()#IntVar作为tikinter的整型变量，能够更新GUI.
track_button=Checkbutton(app,variable=track_playing,command=track_toggle,text=sound_file)
track_button.pack()
#Checkbutton（）创建复选框，可以与tkinter IntVar相关联，设置值为1或者0.
#此处利用track_playing.get()来确定值

app.protocol("WM_DELETE_WINDOW",shutdown)#应用程序窗口app的protocol()方法

app.mainloop()

