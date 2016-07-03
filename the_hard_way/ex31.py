print("you enter blalbla. do you go through door #1 or #2 ?")

door = input("> ")#可以用提示符prompt来做。ex13可能。
if door == "1":
	print("bear eating a cake. what do you do ?")
	print("1. take the cake.")
	print("2. scream at the bear.")
	
	bear = input("> ")
	if bear == "1":
		print("bear eats face off. good job.")
	elif bear == "2":
		print("bear eats legs off. good job.")
	else:
		print("well, doing %s is better. bear runs away." % bear)

elif door == "2":
	print("you stare into the endless abyss.")
	print("1. blueberries.")
	print("2. yellow clothespins.")
	print("3. understanding revolves yelling melodies.")
	
	insanity = input("> ")
	
	if insanity == "1" or insanity == "2":
		print("survives by a mind of jello. good job.")
	else:
		print("insanity rots your eyes into a pool of muck. good job.")
	
else:
	print("you stumble around and fall and die. good job.")