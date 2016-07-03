class animal(object):
	pass

class dog(animal):#不同的类中都定义了相同名字的函数，如何确定调用的哪一个？
	def __init__(self, name):
		self.name = name
		
class cat(animal):
	def __init__(self, name):
		self.name = name
		
class person(object):
	def __init__(self, name):
		self.name = name
		self.pet = None
		
class employee(person):
	def __init__(self, name, salary):
		super(employee, self).__init__(name)
		self.salary = salary
		
class fish(object):
	pass

class salmon(fish):
	pass
	
class halibut(fish):
	pass
	
rover = dog("rover")
satan = cat("satan")
mary = person("mary")