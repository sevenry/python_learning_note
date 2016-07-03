k = input("give the ending number: ")


numbers = []
i = 0
def loop_n(n):
	
	print("at the top i is %d" % i)
	numbers.append(i)

	i = i + 1
	print("numbers now: ", numbers)
	print("at the bottom i is %d" % i)

loop_n(k)
print("the numbers: ")

for num in numbers:
	print(num)
