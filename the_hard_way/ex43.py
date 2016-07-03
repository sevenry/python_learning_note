# 物以类聚节 第二版42
from sys import exit
from random import randint

class Game(object):
	
	def __init__(self, start):
		self.quips = [
			"you died.",
			"mom would be proud.",
			"loser.",
			"puppy."
		]
		self.start = start
		
	def play(self):
		next = self.start
		
		while True:
			print("\n-------")
			room = getattr(self, next)
			next = room()
			
	def death(self):
		print(self.quips[randint(0, len(self.quips)-1)])
		exit(1)
		
	def central_corridor(self):
		print("25# invaded")
		print("last member")
		print("bridge, blow the ship")
		print("escape pod")
		print("\n")
		print("running down the corridor")
		print("a gothon jumps out")
		print("blocking the door")
		print("armory, blast you")
		
		action = input("> ")
		#["shoot!"or"dodge!"or"tell a joke"]
		if action == "shoot!":
			print("quick")
			return 'death'
			
		elif action == "dodge!":
			print("bang your head")
			return 'death'
		
		elif action == "aaa":
			print("lucky")
			return 'laser_weapon_armory'
			
		else:
			print("does not compute")
			return 'central_corridor'
			
	def laser_weapon_armory(self):
		print("get the bomb")
		code = '123'
		#code = "%d%d%d" % (randint(1,9), randint(1,9), randint(1,9)) 
		#当使用这行时，密码本身不可预测，如何保证能猜到密码？以及确保能否调用不报错
		guess = input("[keypad]> ")
		guesses = 0
		
		while guess != code and guesses < 3:#控制尝试密码次数
			print("BZZZZZEDDDD!")
			guesses += 1
			guess = input("[keypad]> ")
			
		if guess == code:
			print("bridge right")
			return 'the_bridge'
		
		else:
			print("you die")
			return 'death'#不同的时候返回的death的输出不一样，这里的是 you died， 之前的就是loser，why？
			
	def the_bridge(self):
		print("burst, dont want to set it off.")
		
		action = input("> ")# python3 就是input，不是raw_input！！！
		
		if action == "throw the bomb.":
			print ("goes off")
			return 'death'
			
		elif action == "place the bomb":
			print ("get off this tin can.")
			return 'escape_pod'
		else:
			print ("does not compute!")
			return "the_bridge"
			
	def escape_pod(self):
		print("5pods. do you take?")
		
		good_pod = randint(1,5)
		guess = input("please guess the code:> ")
		
		if int(guess) != good_pod:
			print("crushing your body")
			return 'death'
		else:
			print("you won!")
			exit(0)
	
a_game = Game("central_corridor")
a_game.play()