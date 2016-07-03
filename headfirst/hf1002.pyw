from tkinter import *
from hf10sound_panel2 import *
import pygame.mixer

    
app=Tk()
app.title("head first mix")

mixer=pygame.mixer
mixer.init()#创建一个mixer对象，并且初始化pygame的声音系统

panel=SoundPanel(app,mixer,"wrong.wav")
panel.pack()
panel=SoundPanel(app,mixer,"correct.wav")
panel.pack()

def shutdown():
    self.track.stop()
    app.destroy()
    
app.protocol("WM_DELETE_WINDOW",shutdown)#利用protocol()方法，并确定调用的函数

app.mainloop()

