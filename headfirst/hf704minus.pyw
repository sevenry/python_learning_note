from tkinter import *

correct_number=0
wrong_number=0

def correct():
    global correct_number
    correct_number=correct_number+1
   
def wrong():
    global wrong_number
    wrong_number=wrong_number+1
   
app=Tk()
app.title("TVN Game Show")
app.geometry('300x100+200+100')

b1=Button(app,text="correct",width=10,command=correct)
b1.pack(side='left',padx=10,pady=10)

b2=Button(app,text="wrong",width=10,command=wrong)
b2.pack(side='right',padx=10,pady=10)

app.mainloop()#缺失()导致主循环没有结束

print(str(correct_number)+" are right")
print(str(wrong_number)+" are wrong")


