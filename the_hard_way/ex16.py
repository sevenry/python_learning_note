from sys import argv
script, filename = argv

print("we're going to erase %r." % filename)#如果输入的是新的文件名，则是重新创建，
#如果输入的是既有文件名就是改写 且filename需要写成xxx.txt，带有文件名格式
print("if you do not want that, hit c.")
print("if you want that, hit return.")

input("?")

print("opening the file...")
target = open(filename, 'w')

print("truncating the file. goodbye!")
target.truncate()

print("now I'm going to ask you for 3 lines.")
line1 = input("line 1: ")
line2 = input("line 2: ")
line3 = input("line 3: ")

print("I'm going to write these to the file")

target.write(line1)
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")

target.write("%r\n %r"%(line1,line2))#并不能用格式化字符实现呀。
#target.write(line1+'\n'+line2)
print("and finally. close.")
target.close()