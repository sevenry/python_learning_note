import random
import math

dorms=['Zeus','Athena','Hercules','Bacchus','Pluto']

prefs=[('Toby', ('Bacchus', 'Hercules')),
       ('Steve', ('Zeus', 'Pluto')),
       ('Karen', ('Athena', 'Zeus')),
       ('Sarah', ('Zeus', 'Pluto')),
       ('Dave', ('Athena', 'Bacchus')), 
       ('Jeff', ('Hercules', 'Pluto')), 
       ('Fred', ('Pluto', 'Athena')), 
       ('Suzie', ('Bacchus', 'Hercules')), 
       ('Laura', ('Bacchus', 'Hercules')), 
       ('James', ('Hercules', 'Athena'))]


domain=[(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]
#print(domain)# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]

def printsolution(vec):
  slots=[]
  
  for i in range(len(dorms)):
    slots+=[i,i]
    #print(slots)#上一行的写法是一次加了两个元素#[0,0,1,1,2,2,3,3,4,4]
    #slots+=[[i,i*i]]#这种写法才是一次加一个数组，每个数组有两个元素

  for i in range(len(vec)):
    x=int(vec[i])
    #print(x)
    dorm=dorms[slots[x]]
    #print(slots[x])
    print (prefs[i][0],dorm)
    
    del slots[x]


def dormcost(vec):
  cost=0
  
  slots=[0,0,1,1,2,2,3,3,4,4]

  for i in range(len(vec)):
    x=int(vec[i])
    dorm=dorms[slots[x]]
    pref=prefs[i][1]
    
    if pref[0]==dorm:
      cost+=0
    elif pref[1]==dorm: 
      cost+=1
    else: 
      cost+=3
 
    del slots[x]
    
  return cost












