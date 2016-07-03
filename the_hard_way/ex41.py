class thething(object):
	def __init__(self):#为什么一定要双下划线才不会出错。如果_init_就不ok啊。
		self.number = 0
		
	def some_function(self):
		print("i got called.")
	
	def add_me_up(self, more):
		self.number += more
		return self.number
	
a = thething()
b = thething()

a.some_function()
b.some_function()

print (a.add_me_up(20))#怎么知道self为自动默认值，需要缺省？
print (b.add_me_up(30))

print(a.number)#把a.number的值返回给a.add_me_up，下面还是可以继续用a.number的表达形式？
print(b.number)

class themultiplier(object):
	def __init__(self, base):
		self.base = base
		
	def do_it(self, m):
		return m * self.base
		
x = themultiplier(a.number)
print(x.do_it(b.number))