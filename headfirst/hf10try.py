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

    global track# 不直接导入模块的话，global是有效的，但是如果导入的话，global即使作为
    #全局变量仍旧只对变量所在模块起作用。
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



app=Tk()
app.title("head first mix")

mixer=pygame.mixer
mixer.init()#创建一个mixer对象，并且初始化pygame的声音系统


def shutdown():
    track.stop()
    app.destroy()
    
mygui = creat_gui(app,mixer,"correct.wav")
mygui2 = creat_gui(app,mixer,"wrong.wav")
#track=mixer.Sound(sound_file)#不加这一行提醒track没有定义，加了就是sound_file没有定义

app.protocol("WM_DELETE_WINDOW",shutdown)#利用protocol()方法，并确定调用的函数

app.mainloop()

