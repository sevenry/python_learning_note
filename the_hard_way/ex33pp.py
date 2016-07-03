i = 0
numbers = []

for i in range(0, 6):
	print("at the top i is %d" % i)
	numbers.append(i)
	i = i + 1 # 无论有没有这一行，循环都是从for开始的，这一行只加了一次，并没有实现不断循环的功能。
	print("numbers now: ", numbers) 
	print("at the bottom i is %d" % i) # 但是会影响这一行的输出i值。
	
print("the numbers: ")

for num in numbers:
	print(num)
