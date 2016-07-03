from tkinter import * #tkinter是内置模块www

def save_data():
    filed=open("deliveries.txt","a")
    filed.write("Depot:\n")
    filed.write("%s\n"%depot.get())
    filed.write("Descripton:\n")
    filed.write("%s\n"%description.get())
    filed.write("Dddress:\n")
    filed.write("%s\n"%address.get("1.0",END))#1.0表示1行0列。行从1开始，列从0开始
    depot.delete(0,END)
    description.delete(0,END)
    address.delete("1.0",END)#delete删除的是gui界面的数据而不是txt的

app=Tk()
app.title('Head-Ex Deliveries')
Label(app,text='Depot:').pack()#不带参数的pack意味着tkinter自动安排最好位置
depot=Entry(app)#Entry 和Text是tkinter库中所带的两种窗口部件 Entry用于单行 Text用于多行
depot.pack()#程序并不知道depot对应的是哪个标签，是人自己对应的“depot”标签对应的那个空
#在save_data里面调用的是depot.pack()，而不是"depot"标签下填的答案
Label(app,text="Description:").pack()
description=Entry(app)
description.pack()
Label(app,text="Dddress:").pack()
address=Text(app)
address.pack()


Button(app,text="save",command=save_data).pack()

app.mainloop()
