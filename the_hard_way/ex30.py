people = 30
cars = 40
buses =15

if cars > people:
	print("we should take the cars.")
elif cars < people:
	print("should not cars.")
else:
	print("we can't decide.")
	
if buses > cars:
	print("too many buses.")
elif buses < cars:
	print("could take the buses.")
else:
	print("still can't decide.")
	
if people > buses:
	print("take the buses.")
else:
	print("stay home.")