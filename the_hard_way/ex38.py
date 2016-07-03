states = {
	"oregen": "or",
	"florida": "fl",
	"california": "ca",
	"new york": "ny",
	"michigan": "mi"
}

cities = {
	"ca": "san francisco",
	"mi": "detroit",
	"fl": "jacksonville",
}

cities["ny"] = "new york"
cities["or"] = "portland"

print("-" * 10)
print("ny state has: ", cities["ny"])       
print("or state has：", cities["or"])

print("-" * 10)
print("michigan's abbreviation is: ", states["michigan"])
print("florida's abbreviation is: ", states["florida"])

print("-" * 10)
print("michigan has: ", cities[states["michigan"]])
print("florida has: ", cities[states["florida"]]) 

print("-" * 10)
for state, abbrev in states.items():
	print("%s is abbreviated %s" % (state, abbrev))
	
print("-" * 10)
for abbrev, city in cities.items():
	print("%s has the city %s" % (abbrev, city))

print("-" * 10)
for state, abbrev in states.items():
	print("%s state is abbreviated %s and has city %s" % (
		state, abbrev, cities[abbrev]))
		
print("-" * 10)
state = states.get("texas", None)

if not state:
	print("sorry, no texas.")# 不懂，不是stetes本身有一堆数据吗。

city = cities.get("tx", "does no exist")
print("the city for the state 'tx' is: %s" % city)#如果是“tx”就需要改成\"tx\"，单引号则不必。