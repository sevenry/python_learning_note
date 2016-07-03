from tkinter import * # import 111 是与111模块相关联，调用其中文件是111.kk
# from 222 import * 是说把222所有的东西化为本模块的东西，可以直接调用其中的文件
# from 222 import ccc 是说从222中调用ccc

app=Tk()
app.title("TVN Game Show")
app.geometry('300x100+200+100')

b1=Button(app,text="correct",width=10)
b1.pack(side='left',padx=10,pady=10)#pack是一种方法确定b1的位置

b2=Button(app,text="wrong",width=10)
b2.pack(side='right',padx=10,pady=10)

app.mainloop
