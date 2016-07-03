from sys import argv
script, filename = argv
txt = open('ex15_sample.txt')#如果直接是filename，则出错，如果'filename'又会提示不存在。如果不加引号无法
#调用，加了引号就成为了确定的名字……囧

print("here's your file %r:" % filename)#%r 输出会有引号，而%s则没有。
print(txt.read())

print("type the filename again:")
file_again = input(">  ")
