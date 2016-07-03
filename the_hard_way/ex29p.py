people = 20
cats = 30
dogs = 15

if (people < cats and True): # 加括号不影响运行的呀~
  print("too many cats!")
  
if people > cats:
  print ("not many cats!")
  
if people < dogs:
  print("the world is drooled on!")
  
if people > dogs:
  print("the world is dry!")
  
dogs += 5

if people >= dogs:
  print("people are greater than or equal to dogs.")
  
if people <= dogs:
  print("people are less than or equal to dogs.")
  
if people == dogs:
  print("people are dogs.")