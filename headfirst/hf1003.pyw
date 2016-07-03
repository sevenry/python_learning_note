from tkinter import *
from hf10sound_panel2 import *
import pygame.mixer
import os # 导入操作系统
    
app=Tk()
app.title("head first mix")

mixer=pygame.mixer
mixer.init()#创建一个mixer对象，并且初始化pygame的声音系统

dirList=os.listdir(".")#是说这个pyw所在文件夹的list？
for fname in dirList:
    if fname.endswith(".wav"):
        panel=SoundPanel(app,mixer,fname)
        panel.pack()

def shutdown():
    track.stop()
    app.destroy()
    
app.protocol("WM_DELETE_WINDOW",shutdown)#利用protocol()方法，并确定调用的函数

app.mainloop()

