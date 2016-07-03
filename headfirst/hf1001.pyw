from tkinter import *
from hf10sound_panel import *
import pygame.mixer

    
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

