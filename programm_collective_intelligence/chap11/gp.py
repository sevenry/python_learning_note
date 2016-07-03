from random import random,randint,choice
from copy import deepcopy
from math import log

class fwrapper:
  def __init__(self,function,childcount,name):
    self.function=function
    self.childcount=childcount
    self.name=name

class node:
  def __init__(self,fw,children):
    #print(fw)
    self.function=fw.function
    self.name=fw.name
    self.children=children

  '''  
  def __lt__(self, y):
    if hasattr(y,"children"):return self.children<y.children
    elif hasattr(y,"idx"):return self.children>y.idx
    #elif hasattr(y,"v"):return self.children>y.v
  '''
  
  def evaluate(self,inp):    
    #print(inp)
    #print(self.children)
    #print(n for n in self.children)
    results=[n.evaluate(inp) for n in self.children]#????递归？
    #print(results)
    #A=self.function(results)
    #print(A)
    return self.function(results)
  
  def display(self,indent=0):
    print ((' '*indent)+self.name)
    for c in self.children:
      c.display(indent+1)
    
class paramnode:
  def __init__(self,idx):
    #print(idx)#0,1,1
    self.idx=idx
  '''
  def __lt__(self, y):
    return self.idx<y.idx'''
  
  def evaluate(self,inp):
    #print(inp[self.idx])
    return inp[self.idx]
  
  def display(self,indent=0):
    print ('%sp%d' % (' '*indent,self.idx))
        
class constnode:
  def __init__(self,v):
    self.v=v
  '''  
  def __lt__(self, y):
    return self.v<y.v
  '''
  def evaluate(self,inp):
    #print(self.v)
    return self.v
  
  def display(self,indent=0):
    print ('%s%d' % (' '*indent,self.v))

addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract') 
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')

def iffunc(l):
  if l[0]>0: return l[1]
  else: return l[2]

ifw=fwrapper(iffunc,3,'if')

def isgreater(l):
  if l[0]>l[1]: return 1
  else: return 0

gtw=fwrapper(isgreater,2,'isgreater')

flist=[addw,mulw,ifw,gtw,subw]

def exampletree():
  #print(gtw,addw,subw)
  #print(paramnode(0))
  #return node(ifw,[0,8,1])
  return node(ifw,[
                  node(gtw,[paramnode(0),constnode(3)]),#传入的变量(0)位与常数3做gtw函数法
                  node(addw,[paramnode(1),constnode(5)]),
                  node(subw,[paramnode(1),constnode(2)]),
                  ]
              )
  
  
def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
  if random()<fpr and maxdepth>0:
    #print(random(),'111')##这样检测是无效的，因为每次random()被调用时，都重新随机一次，所以这里print的随机值和上面的不同。
    f=choice(flist)
    children=[makerandomtree(pc,maxdepth-1,fpr,ppr) 
              for i in range(f.childcount)]
    return node(f,children)
  elif random()<ppr:
    #print(random(),maxdepth,'hhh')
    return paramnode(randint(0,pc-1))
  else:
    return constnode(randint(0,10))

def hiddenfunction(x,y):####这个好像没有用到？
    return x**2+2*y+3*x+5

def buildhiddenset():
  rows=[]
  for i in range(200):
    x=randint(0,40)
    y=randint(0,40)
    rows.append([x,y,hiddenfunction(x,y)])
  return rows


def scorefunction(tree,s):
  dif=0
  for data in s:
    v=tree.evaluate([data[0],data[1]])
    dif+=abs(v-data[2])
  return dif


def mutate(t,pc,probchange=0.1):
  if random()<probchange:#为什么需要这个判断呢。
    #print("tree")
    return makerandomtree(pc)
  else:
    #print("no tree")
    result=deepcopy(t)#不改变t
    if hasattr(t,"children"):#判断对象t是否具有children属性
      result.children=[mutate(c,pc,probchange) for c in t.children]
    return result

def crossover(t1,t2,probswap=0.7,top=1):
  if random()<probswap and not top:#不会执行第一行
    #print("ghh")
    return deepcopy(t2) 
  else:
    result=deepcopy(t1)
    if hasattr(t1,'children') and hasattr(t2,'children'):
      result.children=[crossover(c,choice(t2.children),probswap,0) #在这里改变了top的值。
                       for c in t1.children]
    return result


def evolve(pc,popsize,rankfunction,maxgen=5,
           mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
  def selectindex():
    return int(log(random())/log(pexp))

  population=[makerandomtree(pc) for i in range(popsize)]
  for i in range(maxgen):
    scores=rankfunction(population)
    #scores=rankfunction#这一行是为了有时候传入的直接是函数后的population值
    print(scores[0][0])
    if scores[0][0]==0: break
    
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


def getrankfunction(dataset):
  def rankfunction(population):#evolve中调用getrankfunction的时候把参数传给population。
    scores=[(scorefunction(t,dataset),t) for t in population]#第一项为得分，第二项是树结构
    #print(scores[0:5])#为什么明明可以输出前五个却无法排序呢。
    #print(len(scores))
    #scores.sort()#####why not?????????
    return scores
  return rankfunction


def gridgame(p):
  max=(3,3)
  
  lastmove=[-1,-1]
  
  location=[[randint(0,max[0]),randint(0,max[1])]]
  location.append([(location[0][0]+2)%4,(location[0][1]+2)%4])
  #print(location)
  for o in range(20):#50
  
    for i in range(2):
      #print(location)#每经历一次循环，则location发生一次变化。
      locs=location[i][:]+location[1-i][:]
      a=location[0][:]
      #print(i)
      #print(a)
      #print(locs)
      locs.append(lastmove[i])
      #print(locs)#此时len(locs)为5，所以之前建立树模型的时候，pc=5，需要有五个参数
      move=p[i].evaluate(locs)%4#以4为模，取余
      
      if lastmove[i]==move: return 1-i
      lastmove[i]=move
      if move==0: 
        location[i][0]-=1
        if location[i][0]<0: location[i][0]=0
      if move==1: 
        location[i][0]+=1
        if location[i][0]>max[0]: location[i][0]=max[0]
      if move==2: 
        location[i][1]-=1
        if location[i][1]<0: location[i][1]=0
      if move==3: 
        location[i][1]+=1
        if location[i][1]>max[1]: location[i][1]=max[1]
      
      if location[i]==location[1-i]: return i
  return -1
  
  
def tournament(pl):
  losses=[0 for p in pl]
  
  for i in range(len(pl)):
    for j in range(len(pl)):
      if i==j: continue
      
      winner=gridgame([pl[i],pl[j]])
      
      if winner==0:
        losses[j]+=2
      elif winner==1:
        losses[i]+=2
      elif winner==-1:
        losses[i]+=1
        losses[i]+=1
        pass

  m=zip(losses,pl)
  z=list(m)#
  #print(z)
  z.sort()##sort 函数问题在于 如果losses值相同无法根据树排序。
  #print(z)
  return z      


class humanplayer:
  def evaluate(self,board):

    me=tuple(board[0:2])
    others=[tuple(board[x:x+2]) for x in range(2,len(board)-1,2)]
    
    for i in range(4):
      for j in range(4):
        if (i,j)==me:
          print ('O',)
        elif (i,j) in others:
          print ('X',)
        else:
          print ('.',)
      print()####????
      
    print ('Your last move was %d' % board[len(board)-1])
    print (' 0')
    print ('2 3')
    print (' 1')
    print ('Enter move: ',)
    
    move=int(input())
    return move


class fwrapper:
  def __init__(self,function,params,name):
    self.function=function
    self.childcount=param
    self.name=name
    
#flist={'str':[substringw,concatw],'int':[indexw]}



















