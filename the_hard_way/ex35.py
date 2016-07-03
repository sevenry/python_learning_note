from sys import exit

def gold_room():
	print("this room is full of gold. how much?")
	
	next = input("> ")
	if "0" in next or "1" in next:
		how_much = int(next)
	else:
		dead("learn to type a number.")
		
	if how_much < 50:
		print("not greedy. win!")
		exit(0)#表示程序是正常退出，exit(1)表示是有错误退出
	else:
		dead("greedy bastard!")
		
def bear_room():
	print("bear here.")
	print("a bunch of honey.")
	print("in front of another door.")
	print("how to move the bea?")
	bear_moved = False
	
	while True:
		next = input("> ")
		
		if next == "take honey":
			dead("the bear slaps your face off.")
		elif next == "taunt bear" and not bear_moved:
			print("the bear has moved from the door. you can go.")
			bear_moved = True  # 当再次输入taunt bear的时候，就会运行到下一段，所以这个命令的目的是同样的输入会得到不同的输出。
		elif next == "taunt bear" and bear_moved:
			dead("the bear chews your leg off.")
		elif next == "open door" and bear_moved: #这一句保证直接 open door 命令无法进入gold room，需要首先bear_moved为True才可以。所以得到唯一解。
			gold_room()
		else:
			print("no idea.")

def cthulhu_room():
	print("see the great evil cthulhu.")
	print("go insane.")
	print("do you flee?")
	
	next = input("> ")
	if "flee" in next:
		start()
	elif "head" in next:
		dead("tasty!")
	else:
		cthulhu_room()

def dead(why):
	print(why, "good job!")
	exit(0)
	
def start():
	print("a dark room.")
	print("a door to your right and left.")
	print("which one?")
	
	next = input("> ")
	
	if next == "left":
		bear_room()
	elif next == "right":
		cthulhu_room()
	else:
		dead("you stumble.")
		
start()