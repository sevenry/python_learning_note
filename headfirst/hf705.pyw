from tkinter import *

def wait_finish(channel):
    while channel.get_busy():
        pass


def correct():
    num_good.set(num_good.get()+1)
        
def wrong():
    num_bad.set(num_bad.get()+1)
    
app=Tk()
app.title("TVN Game Show")
app.geometry('300x100+200+100')

num_good=IntVar()
num_good.set(0)# 在整个循环中 set(0)让值变为0，函数调用增加至1，形成0101的序列
num_bad=IntVar()
num_bad.set(0)

lab=Label(app,text='when you are ready, click on the button',height=3)
lab.pack()
#gui中有很多窗口小部件，Label,Drop down list,Text box,Menu,Combo box,Dialog box

lab1=Label(app,textvariable=num_good)
lab1.pack(side='left')

lab2=Label(app,textvariable=num_bad)
lab2.pack(side='right')

b1=Button(app,text="correct",width=10,command=correct)
b1.pack(side='left',padx=10,pady=10)

b2=Button(app,text="wrong",width=10,command=wrong)
b2.pack(side='right',padx=10,pady=10)

app.mainloop()



