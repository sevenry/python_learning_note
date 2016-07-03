from sys import argv
script, user_name = argv#如果不在文中重新确定user_name，则默认打开python ex14.py xxx的时候
#xxx就作为user_name 在后面被调用。
prompt = '>  '#作为用户提示符出现。

print("hi %s, I'm the %s script." % (user_name, script))
print("I'd like to ask you a few questions.")
print("do you like me %s?" % user_name)
likes = input(prompt)

print("where do you live %s?" % user_name)
lives = input(prompt)

print("what kind of computer do you have?")
computer = input(prompt)

print("""
alright, so you said %r about liking me.
you live in %r. not sure where that is.
and you have a %r computer. nice.
"""%(likes, lives, computer))