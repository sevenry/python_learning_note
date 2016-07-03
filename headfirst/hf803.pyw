from tkinter import *

def save_data():
    filed=open("deliveries.txt","a")
    filed.write("Depot:\n")
    filed.write("%s\n"%depot.get())
    filed.write("Descripton:\n")
    filed.write("%s\n"%description.get())
    filed.write("Dddress:\n")
    filed.write("%s\n"%address.get("1.0",END))#1.0表示1行0列。行从1开始，列从0开始
    depot.set(None)
    description.delete(0,END)
    address.delete("1.0",END)#delete删除的是gui界面的数据而不是txt的


app=Tk()
app.title('Head-Ex Deliveries')
Label(app,text='Depot:').pack()#不带参数的pack意味着tkinter自动安排最好位置
depot=StringVar()
depot.set(None)
OptionMenu(app,depot,"cambridge,ma","cambridge,uk","seattle,wa").pack()

Label(app,text="Description:").pack()
description=Entry(app)
description.pack()
Label(app,text="Dddress:").pack()
address=Text(app)
address.pack()


Button(app,text="save",command=save_data).pack()

app.mainloop()
