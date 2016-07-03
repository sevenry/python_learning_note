from tkinter import *
import pygame.mixer

def creat_gui(app,mixer,sound_file):
    def track_toggle():#函数中的函数就是局部函数；复选框事件处理器
        if track_playing.get()==1:
            track.play(loops=-1)
        else:
            track.stop()
            
    def change_volume(v):#滑块事件处理器
        track.set_volume(volume.get())

    #global track 
    track=mixer.Sound(sound_file)    

    track_playing=IntVar()
    track_button=Checkbutton(app,
                             variable=track_playing,
                             command=track_toggle,
                             text=sound_file)
    track_button.pack(side=LEFT)

    volume=DoubleVar()
    volume.set(track.get_volume())#无论如何都搞不懂get_volume()这是固定搭配吗？
    #而且也搞不懂为啥需要这一行otz
    volume_scale=Scale(app,
                       variable=volume,
                       from_=0.0,#from是保留字，不用保留字命名变量
                       to=1.0,#指定最低最高
                       resolution=0.1,#制定解析度，即刻度间隔
                       command=change_volume,
                       label="volume",
                       orient=HORIZONTAL)#左右移动，VERTICAL是上下移动
    volume_scale.pack(side=RIGHT)


