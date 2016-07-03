from sys import argv # 调用kkk.txt好了

script, input_file = argv

def print_all(f):
  print(f.read())
  
def rewind(f):
  f.seek(1)#因为read()运行一次将指针放到了末尾，所以后文中调用read()后需要seek(0)将指针
  #放到起始位置。而readline()不需要的原因是因为顺序输出，每次指针调用到当行的结尾不会影响
  #下一行的读取。
  #其实不是很懂seek的用法。#作为指针移动到某一处？所以不改变内容？
  
def print_a_line(line_count, f):
  print(line_count, f.readline(),end="")#python3中需要用end语句减少换行，而不是逗号。

current_file = open(input_file)

print("1st we print the whole:")
print_all(current_file)

print("\nrewind aha!\n")
rewind(current_file)

print("print 3 lines!")
#因为调用过rewind函数，输出的第一行有缺失，
#但是如果再运行一次all函数输出的还是全部内容
current_line = 1      
 #也就是说seek()函数并没有改变文本内容，
 #但是为什么会影响后面调用同一文本的输出？
print_a_line(current_line, current_file)
#因为这是在调用函数所以添加逗号也不能减少空行，需要到函数内部的print语句中进行修改。
current_line += 1#current_line = current_line + 1 
print_a_line(current_line, current_file)
current_line = current_line + 1
print_a_line(current_line, current_file)
