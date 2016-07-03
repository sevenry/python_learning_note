import time
import random
import math


people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]

destination='LGA'

flights={}

for line in open('scheduledown.txt'):
  origin,dest,depart,arrive,price=line.strip().split(',')
  flights.setdefault((origin,dest),[])

  flights[(origin,dest)].append((depart,arrive,int(price)))
#print(flights[('BOS','LGA')][1])# 调用这行跟test中r中的数字是一样的效果。

def getminutes(t):
  x=time.strptime(t,'%H:%M')
  return x[3]*60+x[4]

def printschedule(r):
  for d in range(int(len(r)/2)):#因为涉及除号，所以需要int
    name=people[d][0]
    origin=people[d][1]
    out=flights[(origin,destination)][int(r[d*2])]#后续在randomoptimizze中调用时，产生的是浮点数。
    ret=flights[(destination,origin)][int(r[d*2+1])]
    print ('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                  out[0],out[1],out[2],
                                                  ret[0],ret[1],ret[2]))
                                                 
def schedulecost(sol):
  totalprice=0
  latestarrival=0
  earliestdep=24*60
  deadtime = '8:00'
  totalfly=0

  for d in range(int(len(sol)/2)):
    origin=people[d][1]
    outbound=flights[(origin,destination)][int(sol[d*2])]
    returnf=flights[(destination,origin)][int(sol[d*2+1])]
    
    totalprice+=outbound[2]
    totalprice+=returnf[2]
    
    a = getminutes(outbound[1])-getminutes(outbound[0])
    b = getminutes(returnf[1])-getminutes(returnf[0])
    #print(a)
    totalfly = 0.5 * (a + b)
    
    c = getminutes(outbound[0])
    d = getminutes(deadtime)
    if c > d:totalprice+=20
    
    if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])#得到最晚到达的时间。
    if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])#得到最早回来的时间。
  
  totalwait=0  
  
  for d in range(int(len(sol)/2)):
    origin=people[d][1]
    #print(origin)
    outbound=flights[(origin,destination)][int(sol[d*2])]
    #print(outbound)
    returnf=flights[(destination,origin)][int(sol[d*2+1])]
    #print(returnf)
      
    totalwait+=latestarrival-getminutes(outbound[1])
    totalwait+=getminutes(returnf[0])-earliestdep  
    
  #print(latestarrival)
  #print(earliestdep)
  if latestarrival<earliestdep: totalprice+=50#书上逻辑判断出错。最早离开的时间晚于最晚到达，才会多出了几个小时，所以要多算一天。
  
  
  return totalprice+totalwait+totalfly
  
def randomoptimize(domain,costf):
  best=999999999
  bestr=None
  for i in range(0,1000):
    
    r=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
    #domain[i][0]=0,domain[i][1]=9(因为每个人有十趟航班可以选择。)改变时，仅需要在test中修改domain的(0,9)即可。
    #print(r)#r如同test中之前给定的s序号；此处用float也不知道在想什么……
    #domain是乘以people*2得到，所以len(domain)刚好与航班总数吻合。
    cost=costf(r)
    
    if cost<best:
      best=cost
      bestr=r 
  return r

def hillclimb(domain,costf):
  sol=[random.randint(domain[i][0],domain[i][1])#这作者也是很任性啊。float，int全不要了otz。
      for i in range(len(domain))]
  #k=0
  #best=999999999
  while 1:
    
    neighbors=[]
    
    for j in range(len(domain)):
      
      if sol[j]>domain[j][0]:
        neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
      if sol[j]<domain[j][1]:
        neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])#源代码这里加减号和书上反过来了。

    current=costf(sol)
    #print(current)
    #print(best)#运行该行时需要添加best=999999
    best=current#可以省去该行，改在while之前添加 best=999999；因为除了初次循环，后来的循环过程中，如果没有打破，
    #cost=当前值且小于best，best=cost，sol也替换为当前序列，current即当前值，可省略一次赋值过程。如果打破，则best和current均保持上一次的结果不变。
    
    #i = 0 
    for j in range(len(neighbors)):
      cost=costf(neighbors[j])
      if cost<best:
        best=cost
        sol=neighbors[j]
        #i= i+1
        #print(i)
        #k=k+1
        
    if best==current:
      #print(k) #i的写法可以根据多少个1知道循环了多少次while，k的写法可以知道总共变更了多少次best。
      break
  return sol
  
def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):#初始的温度值设置成10000不合理，p的初始值往往在0.3左右，还是很难保留下不同方向的选择。
  vec=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
  #print(vec)
  while T>0.1:
    i=random.randint(0,len(domain)-1)

    dir=random.randint(-step,step)
    
    vecb=vec[:]#这一行为什么不直接写成=vec
    #print(vecb)
    #print(dir)
    vecb[i]+=dir
    #print(vecb)
    if vecb[i]<domain[i][0]: #防止为负
      vecb[i]=domain[i][0]
    elif vecb[i]>domain[i][1]: #防止超过9
      vecb[i]=domain[i][1]

    ea=costf(vec)
    eb=costf(vecb)
    p=pow(math.e,(-eb-ea)/T)
    a=random.random()
    #print(a)
    #print(p)#观察比较两个值。
    if (eb<ea or a<p):
      vec=vecb      

    T=T*cool
  return vec

def geneticoptimize(domain,costf,popsize=5,step=1,
                    mutprob=0.2,elite=0.2,maxiter=4):
  
  def mutate(vec):#可能为空。#这个函数真是够糟糕的啊。dorm问题中，domain的最后一项是[0,0]，只能-1调用，不能+1。
    i=random.randint(0,len(domain)-1)#randint(a,b)可以取到a和b值，所以要-1，range(a,b),是从a到b-1，不用减。
    if random.random()<0.5 and vec[i]>domain[i][0]:
      return vec[0:i]+[vec[i]-step]+vec[i+1:] 
    elif vec[i]<domain[i][1]:
      return vec[0:i]+[vec[i]+step]+vec[i+1:]
  
  def mut(vec):#mutate函数逻辑不完成，可能返回为空，出现错误。题目想实现的是频率<0.5时-1，除非原来是0；频率>0.5时+1,除非原来是9.
    i=random.randint(0,len(domain)-1)#dorm问题中，要改成len(domain)-2 虽然减了之后变成-1 没有问题,矩阵中-1就是最后一个数。所以a[-1]和a[0]是一个值,但是不能加。
    if random.random()<0.5: 
      if vec[i]>domain[i][0]:
        return vec[0:i]+[vec[i]-step]+vec[i+1:] 
      else:
        return vec[0:i]+[vec[i]+step]+vec[i+1:]
    else:
      if vec[i]<domain[i][1]:
        return vec[0:i]+[vec[i]+step]+vec[i+1:]
      else:
        return vec[0:i]+[vec[i]-step]+vec[i+1:] 
  
  def crossover(r1,r2):
    i=random.randint(1,len(domain)-2)
    return r1[0:i]+r2[i:]
  
  pop=[]
  
  for i in range(popsize):
    vec=[random.randint(domain[i][0],domain[i][1]) 
         for i in range(len(domain))]
    pop.append(vec)
  #print(pop)
  #print(len(pop))
  
  topelite=int(elite*popsize)
    
  ##pd = 999999  #双##为遗传算法题解题。
  ##mm = 0
  ##while 1 :
  for i in range(maxiter):
    scores=[(costf(v),v) for v in pop]
    #print(scores)
    
    pd = (scores[0][0])
    print(pd)
    scores.sort()#为什么知道是对scores中的第一项进行排序？
    #print(scores.sort())#None 为什么呀。
    ranked=[v for (s,v) in scores]
    #print(ranked)
    pop=ranked[0:topelite]
    #print(len(pop))
    #print(pop)
    
    '''
    if pd == scores[0][0]:
      mm = mm + 1
      print(mm)
    if pd > scores[0][0]:
      mm = 0
      print(mm)
    if mm > 9:
      break
    '''
    while len(pop)<popsize:
      if random.random()<mutprob:

        c=random.randint(0,topelite)
        m=mut(ranked[c])#
        #print(m)#检查报错。
        #print('kill')
        pop.append(m)
        
      else:
      
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        k=crossover(ranked[c1],ranked[c2])
        #print(k)
        #print('eee')
        pop.append(k)
    
    #print(scores[0][0])
    
  return scores[0][1]
  
  
def whatever(domain,costf):#随机爬山
  #这种思路是让每一个随机点得到的best与end比较，如果best更低，则end = best. 
  #如果取消best变量，直接拿得到的最优结果end与其中每一个随机点爬山的结果比较，如果有更好的则替换。
  end=999999999
  a=None
  for i in range(0,5):
    sol=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
    best=999999
    while 1:
    
      neighbors=[]
    
      for j in range(len(domain)): #是从0到len(domain)-1,所以没有超出范围。#应用dorm函数也不需要修改，因为下面两个if语句都不会符合直接跳出。
      
        if sol[j]>domain[j][0]:
          neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
        if sol[j]<domain[j][1]:
          neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])#源代码这里加减号和书上反过来了。

      current=costf(sol)
     
      for j in range(len(neighbors)):
        cost=costf(neighbors[j])
        if cost<best:
          best=cost
          sol=neighbors[j]
       
      if best==current:
        break
    
    #print(best)
    if best<end:
      end=best
      a=sol
    
  #print(end)
  return a

def maybetry(domain,costf):#随机爬山//字典
  pop=[]
  for i in range(0,100):
    sol=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
    best=999999  #在这种方法中，调用字典来存储每一个随机点附近得到的最优解，则不需要把best放在for外面。
    #因为这样的话，很多随机点产生的结果不如外面的替换的best，将会存储在scores中有很多重复。
    while 1:
    
      neighbors=[]
    
      for j in range(len(domain)):
      
        if sol[j]>domain[j][0]:
          neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
        if sol[j]<domain[j][1]:
          neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])#源代码这里加减号和书上反过来了。

      current=costf(sol)
     
      for j in range(len(neighbors)):
        cost=costf(neighbors[j])
        if cost<best:
          best=cost
          sol=neighbors[j]
       
      if best==current:
        pop.append(sol)
        #print(pop)
        break
     
  scores=[(costf(v),v) for v in pop]
  #print(len(scores))#是for i in range(0,N)的N
  scores.sort()#为什么知道是对scores中的第一项进行排序？

  return scores[0][1]
  

def difftoname(domain,costf,T=10000.0,cool=0.95,step=1):#随机退火
  pop=[] 
  best = 999999
  for i in range(0,100):
    vec=[float(random.randint(domain[i][0],domain[i][1])) 
         for i in range(len(domain))]
    while T > 0.1:
      i=random.randint(0,len(domain)-1)

      dir=random.randint(-step,step)
      vecb=vec[:]#数组是可变的，用这样的表达方式保持原来的vec不随着vecb变化而变化。
      
      vecb[i]+=dir
      
      if vecb[i]<domain[i][0]: 
        vecb[i]=domain[i][0]
      elif vecb[i]>domain[i][1]: 
        vecb[i]=domain[i][1]

      ea=costf(vec)
      eb=costf(vecb)
      p=pow(math.e,(-eb-ea)/T)
      a=random.random()
    
      if (eb<ea or a<p):
        vec=vecb      
        #print(vec)
      T=T*cool
      
    
    if costf(vec)<best:
      best = costf(vec)
      kk = vec
      
  return kk
  '''
    
    pop.append(vec)
    
  scores=[(costf(v),v) for v in pop]
  scores.sort()#为什么知道是对scores中的第一项进行排序？
  print(len(scores))
  return scores[0][1]
  '''
  
  
 





