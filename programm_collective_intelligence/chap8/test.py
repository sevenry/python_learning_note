#####ebay网搜信息依旧有问题啊啊啊啊啊


'''
import numpredict

a=numpredict.wineprice(95.0,3.0)
b=numpredict.wineprice(95.0,8.0)
c=numpredict.wineprice(99.0,1.0)
print(a,b,c)
data=numpredict.wineset1()
#print(data[0])
#print(data[1])
#print(data[2])

print(data[0]['input'])
print(data[1]['input'])
a = numpredict.euclidean(data[0]['input'],data[1]['input'])
print(a)


data=numpredict.wineset1()
#numpredict.knnestimate(data,(95,3))
#numpredict.knnestimate(data,(99,3))
c=numpredict.knnestimate(data,(99,5))
print(c)
b=numpredict.wineprice(99,5)
print(b,"hh")
#print(numpredict.knnestimate(data,(99,5),k=15))
print(numpredict.weightedknn(data,(99,5)))

#print(numpredict.subtractweight(1))
#print(numpredict.inverseweight(3))
#print(numpredict.gaussian(3))


data=numpredict.wineset1()#199
#print(numpredict.crossvalidate(numpredict.knnestimate,data))
def knn3(d,v):return numpredict.knnestimate(d,v,k=3)#前三名进行排列，knn中是前五名。
print(numpredict.crossvalidate(knn3,data))
#def knn1(d,v):return numpredict.knnestimate(d,v,k=1)
print(numpredict.crossvalidate(knn1,data))


data=numpredict.wineset1()
print(numpredict.crossvalidate(numpredict.weightedknn,data))#200
def knninverse(d,v):
  return numpredict.weightedknn(d,v,weightf=numpredict.inverseweight)

print(numpredict.crossvalidate(knninverse,data))


data=numpredict.wineset2()#201
def knn3(d,v):return numpredict.knnestimate(d,v,k=3)#前三名进行排列，knn中是前五名。
#print(numpredict.crossvalidate(knn3,data))
#print(numpredict.crossvalidate(numpredict.weightedknn,data))


data=numpredict.wineset2()
sdata=numpredict.rescale(data,[10,10,0,0.5])
#print(numpredict.crossvalidate(knn3,sdata))
print(numpredict.crossvalidate(numpredict.weightedknn,sdata))


import optimization
costf = numpredict.createcostfunction(numpredict.knnestimate,data)#在调用这个函数的时候，如何知道把新的参数传给内部的函数呢。
#costf= numpredict.new(numpredict.knnestimate,data)#这样写的时候会说new函数确实一项sol参数。
#第五章的时候直接是函数名，函数参数缺省没问题的原因是内部调用函数的时候给了参数。并且比较的就是哪一组参数得到的结果最优。
#a=optimization.annealingoptimize(numpredict.weightdomain,costf,step=2)
a=optimization.maybetry(numpredict.weightdomain,costf)

print(a)
sdata=numpredict.rescale(data,a)
print(numpredict.crossvalidate(numpredict.weightedknn,sdata))

data=numpredict.wineset3()#205
print(numpredict.wineprice(99,20))
#print(numpredict.weightedknn(data,[99,20]))

print(numpredict.probguess(data,[99,20],40,80))#206
print(numpredict.probguess(data,[99,20],80,120))
print(numpredict.probguess(data,[99,20],120,1000))
print(numpredict.probguess(data,[99,20],30,120))

from pylab import *
a=array([1,2,3,4])
b=array([4,2,3,4])
plot(a,b)
show()
#t1=arange(0,10,0.1)
#plot(t1,sin(t1))
#show()


data=numpredict.wineset3()#205
#numpredict.cumulativegraph(data,(99,20),120)

numpredict.probabilitygraph(data,(99,20),120)



###########
import ebaypredict
laptops=ebaypredict.doSearch('beauty')
print(laptops[0:10])#空集呀。
print(ebaypredict.getCategory('computers'))#none…………………………??????why


'''


######习题2
import numpredict
data=numpredict.wineset1()
#data=[{1,2},{2,3},{3,4}]
l=numpredict.leaveoneout(numpredict.weightedknn,data)
print(l)


