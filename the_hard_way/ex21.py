def add(a, b):
  print("adding %d + %d" % (a, b))
  return a + b

def substract(a, b):
  print("substracting %d -%d" % (a, b))
  return a - b 
  
def multiply(a, b):
  print("multiplying %d * %d" % (a, b))
  return a * b

def divide(a, b):
  print("dividing %d / %d" % (a, b))
  return a / b

print("do math!")

age = add(30, 5)
height = substract(78, 4)
weight = multiply(90, 2)
iq = divide(100, 2)#每次调用函数的时候就会print函数中的内容，但是返回的值并没有要求输出，只是赋值给对应的变量。
#python3中除法自动变成浮点数w
print("age: %d, height: %d, weight: %d, iq: %d" % (age, height, weight, iq))#调用变量才知道函数的结果。

print("PUZZLE!")
print(iq)
what = divide(iq, 2)#按照调用的顺序依次输出函数内容
print (type(what))
print("that becomes: ", what, "can you?")
print(type(what))