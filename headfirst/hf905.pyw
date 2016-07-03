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

def change_volume(v):# 改成change_volume(v)也一样可以运行，书上为啥要加v？
    track.set_volume(volume.get())
    
app=Tk()
app.title("head first mix")
#app.geometry('250x100+200+100') 删除这一行让tkinter自动决定GUI尺寸

mixer=pygame.mixer
mixer.init()

sound_file="correct.wav"
track=mixer.Sound(sound_file)

track_playing=IntVar()#IntVar作为tkinter的整型变量，能够更新GUI.
track_button=Checkbutton(app,
                         variable=track_playing,
                         command=track_toggle,
                         text=sound_file)
track_button.pack(side=LEFT)

volume=DoubleVar()#DoubleVar()作为tkinter的浮点数变量，还有StringVar
#volume.set(track.get_volume())####set_volume()是pygame的一种方法，set()是啥意思啊？
#而且看不懂这一行作用是啥唉 感觉去除了之后好像还是能用
volume_scale=Scale(app,#Scale是tkinger的窗口小部件
                   variable=volume,
                   from_=0.0,#from是保留字，不用保留字命名变量
                   to=1.0,#指定最低最高
                   resolution=0.1,#制定解析度，即刻度间隔
                   command=change_volume,#仅仅作为事件驱动才把函数放在=右边
                   label="volume",
                   orient=HORIZONTAL)#左右移动，VERTICAL是上下移动
volume_scale.pack(side=RIGHT)

app.protocol("WM_DELETE_WINDOW",shutdown)#应用程序窗口app的protocol()方法
app.mainloop()

