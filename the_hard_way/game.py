class Room(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.paths = {}
		
	def go(self, direction):
		return self.paths.get(direction, None)#None的作用是？
		
	def add_paths(self, paths):
		self.paths.update(paths)# update不需要return？