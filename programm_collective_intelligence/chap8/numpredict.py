from random import random,randint
import math

def wineprice(rating,age):#根据rating和age得到price
  peak_age=rating-50
  
  price=rating/2
  if age>peak_age:
    price=price*(5-(age-peak_age)/2)
    #print("hhh")
  else:
    price=price*(5*((age+1)/peak_age))
    #print("kkk")
  if price<0: price=0
  return price

def wineset1():#生成数据的方式1
  rows=[]
  for i in range(300):
    rating=random()*50+50
    age=random()*50

    price=wineprice(rating,age)
    
    price*=(random()*0.4+0.8)#噪声设置的目的是啥呀。

    rows.append({'input':(rating,age),
                 'result':price})
  return rows

def euclidean(v1,v2):
  d=0.0
  for i in range(len(v1)):
    d+=(v1[i]-v2[i])**2
  return math.sqrt(d)

def getdistances(data,vec1):#针对某一个数据，data中所有数据按照input之间距离远近排列##并且提取了input的部分。
  distancelist=[]
  
  for i in range(len(data)):
    vec2=data[i]['input']
    
    distancelist.append((euclidean(vec1,vec2),i))#i的作用是标记序列号
  #m=len(data)-1
  #print(distancelist[m][0])
  #print(distancelist[m][1])
  
  distancelist.sort()
  #print(distancelist[m][1])
  return distancelist

def knnestimate(data,vec1,k=5):#从数据中得到某一个input的result的预测。
  dlist=getdistances(data,vec1)
  avg=0.0
  
  for i in range(k):
    idx=dlist[i][1]#得到原来data中的顺序以得到resul值。每个data有着i的序列号和input，result
    #print(idx)
    avg+=data[idx]['result']
  avg=avg/k
  return avg

def inverseweight(dist,num=1.0,const=0.1):#反函数
  return num/(dist+const)

def subtractweight(dist,const=1.0):#减法函数
  if dist>const: 
    return 0
  else: 
    return const-dist

def gaussian(dist,sigma=1.0):#高斯函数，sigma是1，书上有误。
  return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gaussian):#加权knn
  dlist=getdistances(data,vec1)
  avg=0.0
  totalweight=0.0
  
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]
    weight=weightf(dist)
    #print(weight)
    avg+=weight*data[idx]['result']#仅仅是针对距离远近得到加权值而已。
    totalweight+=weight
  if totalweight==0: return 0
  avg=avg/totalweight
  return avg

def dividedata(data,test=0.05):#把数据分为训练级和测试级。训练集用于训练数据，然后将测试级的input输入，
#根据得到的结果与data中的价格进行比对。
  trainset=[]
  testset=[]
  for row in data:
    if random()<test:
      testset.append(row)
    else:
      trainset.append(row)
  return trainset,testset

def testalgorithm(algf,trainset,testset):
  error=0.0
  if len(testset)==0:return 0 #书上没有，自己加的。
  for row in testset:
    guess=algf(trainset,row['input'])
    error+=(row['result']-guess)**2
  return error/len(testset)#没有考虑testset为空的情况。

def crossvalidate(algf,data,trials=100,test=0.1):#得到测试组的误差数值
  error=0.0
  for i in range(trials):#把error的计算方法循环一百遍，是想对数据进行若干组不同的测试组与训练组划分，每种划分再求误差。
    trainset,testset=dividedata(data,test)
    #print(len(testset))
    a=testalgorithm(algf,trainset,testset)
    #print(a)
    error+=a
  return error/trials

def wineset2():#生成data的方式2
  rows=[]
  for i in range(30):
    rating=random()*50+50
    age=random()*50
    aisle=float(randint(1,20))
    bottlesize=[375.0,750.0,1500.0][randint(0,2)]#书上和源代码不符合，根据书上结果不应该有3000这一项。
    #print(bottlesize)#结果是从三个数据中随机选取其中之一
    price=wineprice(rating,age)
    price*=(bottlesize/750)
    price*=(random()*0.2+0.9)#这里依旧参考源代码，书上0.2和0.9的顺序应有误。
    rows.append({'input':(rating,age,aisle,bottlesize),
                 'result':price})
  return rows

def rescale(data,scale):
  scaleddata=[]
  #i=0
  #print('hhh')
  for row in data:
    #i=i+1
    scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
    #if i==1:print(row['input'],scaled)
    scaleddata.append({'input':scaled,'result':row['result']})
  return scaleddata

def createcostfunction(algf,data):
  def costf(scale):
    sdata=rescale(data,scale)
    return crossvalidate(algf,sdata,trials=10)
  return costf

weightdomain=[(0,20)]*4

def new(algf,data,sol):####想改进上一个函数然而失败。
  sdata=rescale(data,sol)
  ans=crossvalidate(algf,sdata,trials=10)
  return ans    

def wineset3():
  rows=wineset1()
  for row in rows:
    if random()<0.5:#考虑从折扣店买
      row['result']*=0.6
  return rows

def probguess(data,vec1,low,high,k=5,weightf=gaussian):#返回酒价格在某个范畴内的概率
  dlist=getdistances(data,vec1)
  nweight=0.0
  tweight=0.0
  
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]#序列标号
    weight=weightf(dist)
    v=data[idx]['result']
    
    if v>=low and v<=high:
      nweight+=weight
    tweight+=weight
  if tweight==0: return 0
  
  return nweight/tweight

from pylab import *

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
  t1=arange(0.0,high,0.1)
  cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])#因为v是在不断增加的，而probguess函数中的high就是v，所以得到的是累积型函数。
  plot(t1,cprob)
  show()

def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
  t1=arange(50,high,0.1)
  
  probs=[probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]
  
  smoothed=[]
  for i in range(len(probs)):#做高斯平滑处理
    sv=0.0
    for j in range(0,len(probs)):
      dist=abs(i-j)*0.1
      weight=gaussian(dist,sigma=ss)
      sv+=weight*probs[j]
    smoothed.append(sv)
  smoothed=array(smoothed)
    
  plot(t1,smoothed)
  show()

def leaveoneout(algf, data):#习题2的留一式交叉验证
  error = 0.0
  for row in data:
    trainset=[]
    for nrow in data:
      if nrow!=row:trainset.append(nrow)
    #print(trainset)
    guess=algf(trainset,row['input'])
    error+=(row['result']-guess)**2
  return error/len(data)
    
  
    
    



