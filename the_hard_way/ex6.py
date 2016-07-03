x = "there are %d types of people." % 10
binary = "binary"
do_not = "don't"
y = "those who know %d and those who %d." % (binary, do_not)

print(x)
print(y)

print("i said: %r." % x)
print("i also said: '%s'." % y)# 如果删去‘’，则输出这句话中没有引号。但是上一句话仍旧有。%r 和 %s差异导致？

hilarious = False
joke_evaluatoin = "isn't that joke so funny? %r"

print(joke_evaluatoin % hilarious)# 等同于print("isn't that joke so funny? %r" % hilarious)

w = "this is the left side of ..."
e = "a string with a right side."

print (w+e)