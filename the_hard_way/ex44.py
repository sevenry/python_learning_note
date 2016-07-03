class parent(object):
	def override(self):
		print("parent override()")
	def implicit(self):
		print("print implicit()")
	def altered(self):
		print("parent altered()")
		
class child(parent):
	def override(self):
		print("child override()")
	#def implicit(self):  如果 class  child (object) ,可以通过重新定义函数并pass的方式来继承
	#	pass
	def altered(self):
		print("child, before parent altered()")
		super(child, self).altered()#但是（object）的话super无法传递
		print("child, after parent altered()")
		
dad = parent()
son = child()

dad.implicit()
son.implicit()
dad.override()
son.override()
dad.altered()
son.altered()