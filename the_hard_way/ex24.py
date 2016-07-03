print("PRACTICE!")
print("you\'d need to know \'bout escape with \\ that do \n newlines and \t tabs.")
#\' 为单引号；\"为双引号；
poem = """
\tthe lovely world
with logic so firmly planted
cannot discern \n the needs of love
nor comprehend passion from intuition
and requires an explanation
\n\t\twhere there is none.
"""

print("-------------")
print(poem)
print("-------------")

five = 10 - 2 + 3 - 6
print("this five: %s" % five) 

def secret_formula(started):
  jelly_beans = started * 500#这里是jellt_beans
  jars = jelly_beans / 1000
  crates = jars / 100
  return jelly_beans, jars, crates
  
start_point = 10000
beans, jars, crates = secret_formula(start_point)#这里是beans，但其实没有关系的。因为只要把函数里的三个值返回给对应的三个变量就可以了，名字怎么样都可以。

print("starting point: %d" % start_point)
print("we have %d beans, %d jars, %d crates." % (beans, jars, crates))

start_point = start_point / 10

print("also do that:")
print("we have %d beans, %d jars, %d crates." % secret_formula(start_point))
