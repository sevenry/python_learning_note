from tkinter import *

app=Tk()
app.title("TVN Game Show")
app.geometry('300x100+200+100')

def button_click():
    print("i have be clicked! ")

b=Button(app,text="click on me",width=10,command=button_click)
b.pack(padx=10,pady=10)

b1=Button(app,text="correct",width=10)#Button 和Tk都是tkinter中含有的？
b1.pack(side='left',padx=10,pady=10)#pack是一种方法确定b1的位置

b2=Button(app,text="wrong",width=10)
b2.pack(side='right',padx=10,pady=10)

app.mainloop
