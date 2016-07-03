from sys import argv
script, filename = argv
txt = open(filename)#如果直接是filename，则出错，
#如果'filename'又会提示不存在。如果不加引号无法
#调用，加了引号就成为了确定的名字……囧,比书上多加了‘r’就能运行了，
#但是改名字再打开就不行了。
#需要加后缀名啦~

print("here's your file %r:" % filename)#%r 输出会有引号，而%s则没有。
print(txt.read())

print("type the filename again:")
file_again = input(">  ")

txt_again = open(file_again)#不过话说我也没看懂这里为什么有改变文件名的地方啊。

print(txt_again.read())