from tkinter import *

def save_data():
    filed=open("deliveries.txt","a")
    filed.write("Depot:\n")
    filed.write("%s\n"%depot.get())
    filed.write("Descripton:\n")
    filed.write("%s\n"%description.get())
    filed.write("Dddress:\n")
    filed.write("%s\n"%address.get("1.0",END))#1.0表示1行0列。行从1开始，列从0开始
    depot.set(None)#保证清空
    description.delete(0,END)
    address.delete("1.0",END)#delete删除的是gui界面的数据而不是txt的

def read_depots(file):
    depots=[]
    depots_f=open(file)
    for line in depots_f:
        depots.append(line.rstrip())#把去掉换行符后的行拷贝添加到数组里
    return depots



app=Tk()
app.title('Head-Ex Deliveries')
Label(app,text='Depot:').pack()#不带参数的pack意味着tkinter自动安排最好位置
depot=StringVar()
depot.set(None)
options=read_depots("depots.txt")
OptionMenu(app,depot,*options).pack()

Label(app,text="Description:").pack()
description=Entry(app)
description.pack()
Label(app,text="Dddress:").pack()
address=Text(app)
address.pack()


Button(app,text="save",command=save_data).pack()

app.mainloop()
