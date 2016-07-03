name = 'zed'
age = 23
height = 74
weight = 180
eyes = 'blue'
teeth = 'white'
hair = 'brown'

print("let's talk about us %s." % name)
print("he's %s inches tall." % (10*height))#改变单位之间的转换方式。如果直接变成10*height，会重复输出10次。
print("he's %s pounds heavy." % weight)#%s和%r区别在于，如果weight=‘hello，world’，前者是hello，后者是全文
print("actually that's not too heavy.")
print("he's got %s eyes and %s hair." % (eyes, hair))
print("his teeth are usually %s depending on the coffee." % teeth)

print("if i add %d, %d, and %d i get %d." % (age, height, weight, age + height + weight))