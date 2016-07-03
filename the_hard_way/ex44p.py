class other(object):
	def override(self):
		print("other override()")
	def implicit(self):
		print("other implicit()")
	def altered(self):
		print("other altered()")
		
class child(object):# 没有使用（other）
	def __init__(self):
		self.other = other() #初始化w
	def implicit(self):
		self.other.implicit()
	def override(self):
		print("child override()")
	def altered(self):
		print("child, before parent altered()")
		self.other.altered()
		print("child, after parent altered()")
		
son = child()

son.implicit()

son.override()

son.altered()