def print_two(*args):
  arg1, arg2 = args 
  print("arg1: %r, arg2: %r" % (arg1, arg2))
  #如果把arg1换成kk也不会有问题。
  
def print_two_again(args1, args2):
#并不是定义的问题，args并不具有特定的含义唉。随便换成其他名字也没问题。
  print("arg1: %s, arg2: %s" % (args1, args2))
  
def print_one(arg1):
  print("arg1: %r" % arg1)
  
def print_none():
  print("i got nothing.")
  
print_two("z","shaw")
print_two_again("z","k")
#为什么无法输出？省去这一行就没有问题囧。
print_one("first!")
print_none()