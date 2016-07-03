####关于sort的问题。如果数值相同，后面都是树，如何排序？


import gp
'''
exampletree = gp.exampletree()#278
#print(exampletree)
#print(exampletree.evaluate([2,3]))#实际是把2,3两个数带到exampletree中每一个函数进行运算。
#print(exampletree.evaluate([5,4]))

#node 类中添加display##278
#exampletree.display()#

random3=gp.makerandomtree(2)#280
#print(random3.evaluate([7,1]))
#print(random3.evaluate([2,4]))

random4=gp.makerandomtree(2)
#print(random4.evaluate([5,3]))
#print(random4.evaluate([5,20]))

#random3.display()
#random4.display()



####检测random###makerandomtree函数中使用。
from random import random
if random()<0.5:
    print("hhh",random())
else:
    print("kkk",random())


hiddenset=gp.buildhiddenset()#282
#print(gp.scorefunction(random4,hiddenset))
#print(gp.scorefunction(random3,hiddenset))

random4.display()#284 
print('______')
muttree=gp.mutate(random4,2)
for i in range(16):
    muttree=gp.mutate(muttree,2)
muttree.display()

print(gp.scorefunction(random4,hiddenset))
print(gp.scorefunction(muttree,hiddenset))

from random import random
random1=gp.makerandomtree(2)#286
#random1.display()
print('-------')
random2=gp.makerandomtree(2)
#random2.display()
print('-------')
cross=gp.crossover(random1,random2)
#cross.display()
###检测 crossover的and not
279
a=1
b=4
if random()<0.5 and not  a:
    b=b-1
    print(b)
    
    

#######sth wrong crycrycrycry？？？？？
rf=gp.getrankfunction(gp.buildhiddenset())#289
gp.evolve(2,500,rf,mutationrate=0.2,breedingrate=0.1,pexp=0.7,pnew=0.1)


######检查sort函数
a=[(1,('ab')),(1,('ac')),(1.4,('ew'))]
a.sort()
print(a)


p1=gp.makerandomtree(5)#292
p2=gp.makerandomtree(5)
#p1.display()
print(gp.gridgame([p1,p2]))

for i in range(1):
    print(i)
aa=gp.makerandomtree(5)
#population=[gp.makerandomtree(5) for i in range(2)]
#kk=gp.tournament(population)
#print(kk[0][0])
#print(kk)
#winner=gp.evolve(2,100,kk,maxgen=50)#这个在evolve函数中需要调用#行。
#winner=gp.evolve(2,100,gp.tournament,maxgen=50)#293

gp.gridgame([aa,gp.humanplayer()])#294

'''
from random import random,randint,choice

a=[1,2,3,4,5]
a.append(6)
b=choice(a)
#print(b)
for i in a:
    print(i)

random1=gp.makerandomtree(2)#286
random1.display()
print('-------')
random2=gp.makerandomtree(2)
random2.display()
print('-------')
cross=gp.crossover(random1,random2)
cross.display()
    
'''
####习题1
def distance(a,b):
  dis=(a[0]-b[0])^2+(a[1]-b[1])^2
  return dis
disw=fwrapper(distance,4,'dis')

####习题3
def crossover(t1,t2,probswap=0.7,top=1):
  if random()<probswap and not top:#不会执行第一行
    #print("ghh")
    return deepcopy(t2) 
  else:
    result=deepcopy(t1)
    child=t2.children
    child.append(t2)
    if hasattr(t1,'children') and hasattr(t2,'children'):
      result.children=[crossover(c,choice(child),probswap,0) #在这里改变了top的值。
                       for c in t1.children]
    return result

    
######习题4
def evolve(pc,popsize,rankfunction,maxgen=5,
           mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
  def selectindex():
    return int(log(random())/log(pexp))
  
  kk=9999999999999
  count=0
  
  population=[makerandomtree(pc) for i in range(popsize)]
  for i in range(maxgen):
    scores=rankfunction(population)
    #scores=rankfunction#这一行是为了有时候传入的直接是函数后的population值
    print(scores[0][0])
    if scores[0][0]==0: break
    
    ###终止变异法
    if kk>scores[0][0]:
      kk=scores[0][0]
      count=0
    else:count+=1
    if count>10:break
    
    newpop=[scores[0][1],scores[1][1]]
    
    while len(newpop)<popsize:
      if random()>pnew:
        newpop.append(mutate(
                      crossover(scores[selectindex()][1],
                                 scores[selectindex()][1],
                                probswap=breedingrate),
                        pc,probchange=mutationrate))
      else:
        newpop.append(makerandomtree(pc))
        
    population=newpop
  scores[0][1].display()    
  return scores[0][1]
'''
