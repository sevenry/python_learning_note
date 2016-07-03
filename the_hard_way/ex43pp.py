#这个才是真正的哥顿星人那一节啊望天。第二版的41节。
from sys import exit
from random import randint

def death():
	quips = ["you died. you kinda suck at this.",
			"nice job, you died... ",
			"such a loser.",
			"i have a small puppy."]
			
	print(quips[randint(0, len(quips)-1)])
	exit(1)
	
def central_corridor():
	print("gothons and blahblah and blast you.")
	
	action = input(">")
	
	if action == "shoot!":
		print("you are dead.")
		return 'death'
	
	elif action == "dodge!":
		print("gothons eat you. ")
		return 'death'
		
	elif action == "joke":
		print("armory door.")
		return 'laser_weapon_armory'
		
	else:
		print("does not compute!")
		return 'central_corridor'
		
def laser_weapon_armory():
	print("get the bomb. the code is 3 digits.")
	#code = 123 当直接将密码存为数字的时候，后面需要分别改成 while int(guess) 和 if int(guess)
	#如果只改了while 语句 而没有修改if 语句猜中数字，则while的三次机会也将失效，直接跳入die 语句。
	#将陷入猜中了答案却都不能调用等于和不等于两种情况，因为本身字符串无法与code 的123 数值匹配。
	code = "123"
	#code = "%d%d%d" % (randint(1,9), randint(1,9), randint(1,9))
	guess = input("[keypad]> ")
	guesses = 0
	
	while guess != code and guesses < 3:
		print("BZZZZZEDDDDD!")
		guesses += 1
		guess = input("[keypad]> ")#这段代码是保证第四次及以后即使猜对也无用
		
	if guess == code:
		print ("right spot")
		return 'the_bridge'
	else:
		print("you die.")
		return 'death'
		
def the_bridge():
	print("don't want to set it off.")
	
	action = input(">")
	
	if action == "throw the bomb":
		print("it goes off.")
		return 'death'
		
	elif action == "place the bomb":
		print("you escaped.")
		return 'escape_pod'
		
	else:
		print(" does not compute!")
		return 'the_bridge'
		
def escape_pod():
	print("5 pods, do you take?")
	
	good_pod = randint(1,5)
	guess = input("[pd #]> ")
	
	if int(guess) != good_pod:
		print("jam jelly.")
		return 'death'
	else:
		print("you won!")
		exit(0)
		
rooms = {
	'death': death,
	'central_corridor': central_corridor,
	'laser_weapon_armory': laser_weapon_armory,
	'the_bridge': the_bridge,
	'escape_pod': escape_pod
}

def runner(map, start):# 不太懂这段及上面这段。
	next = start
	
	while True:
		room = map[next]
		print("\n--------")
		next = room()
		
runner(rooms, 'central_corridor')