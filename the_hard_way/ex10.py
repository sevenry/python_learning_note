tabby_cat = "\tI'm tabbed in."
persian_cat = "I'm split\non a line."
backslash_cat = "I'm \\ a \\ cat."

fat_cat = """
I'll do a list:
\t* cat food
\t* fishes
\t* catnip\n\t* grass
"""

print(tabby_cat)
print(persian_cat)
print(backslash_cat)
print(fat_cat)


for i in ["/",'-','|','\\','|']:
  print("%r\r" % i),
