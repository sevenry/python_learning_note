####11111

import optimization


#s = [1,4,3,2,7,3,6,3,2,4,5,3]

#domain = [(0,9)] * (len(optimization.people) * 2)
#print(domain)

#a = optimization.randomoptimize(domain, optimization.schedulecost)#随机法
#b = optimization.hillclimb(domain, optimization.schedulecost)#爬山法
#c= optimization.annealingoptimize(domain, optimization.schedulecost)#模拟退火法
#a = optimization.geneticoptimize(domain, optimization.schedulecost)#遗传算法
#a = optimization.whatever(domain, optimization.schedulecost)#随机爬山法
#a= optimization.maybetry(domain, optimization.schedulecost)

#a= optimization.difftoname(domain, optimization.schedulecost)



#注意append用法：a=[];a.append(bbb) print(a[i])

'''
print(a)
print(optimization.schedulecost(a))
optimization.printschedule(a)

#######22222 需要联网otz

import kayak
sid = kayak.getkayaksession()
searchid = kayak.flightsearch(sid,'BOS','LGA','11/17/2006)
f = kayak.flightsearchresults(sid, searchid)
f[0:3]



#######333333
import dorm

#dorm.printsolution([0,0,0,0,0,0,0,0,0,0])#调用遗传法，mut里最后一项可能是1，这里最后一项是1会报错，所以不能随便加减的。

#s = optimization.randomoptimize(dorm.domain, dorm.dormcost)#随机数法真是非常非常非常糟糕啊。在分寝室的问题中，1000的频数的结果还是很不理想。

#s = optimization.geneticoptimize(dorm.domain, dorm.dormcost)

s = optimization.whatever(dorm.domain, dorm.dormcost)

#s = optimization.hillclimb(dorm.domain, dorm.dormcost)
print(s)
print(dorm.dormcost(s))
dorm.printsolution(s)



##########4444444
import socialnetwork
#s = optimization.randomoptimize(socialnetwork.domain, socialnetwork.crosscount)
s = optimization.whatever(socialnetwork.domain, socialnetwork.crosscount)

print(s)
print(socialnetwork.crosscount(s))
socialnetwork.drawnetwork(s)


i =6 
def sss(i):
    i=i+4
    print(i)
a=sss(i)    
print(i)

import random
i=random.randint(0,2)
print(i)


for i in range(4):
  print(i)

a=[0]
print(a[0])
print(a[-1])


aa=[]
bb=[]
cc=[]
for i in range(3):
    aa+=[i,i*i]
    print(aa)
    bb+=[[i,i*i]]
    print(bb)
    cc+=[i,[i*i]]
    print(cc)
    

a=[1,2,3,4,5,6]
b=a[:]
print(b)


#######习题室友。
import dormex

#a = [[0,1],[2,3],[4,5],[6,7],[8,9]]
#a=[0,0,0,0,0,0,0,0,0,0]
#a=[9,8,7,6,5,4,3,2,1,0]
#print(dormex.domain)
#a = optimization.randomoptimize(dormex.domain, dormex.matecost)
#a = optimization.hillclimb(dormex.domain, dormex.matecost)
a = optimization.whatever(dormex.domain, dormex.matecost)
#a = optimization.difftoname(dormex.domain, dormex.matecost)
s = dormex.printresult(a)

print(dormex.matecost(a))

#dormex.kk()
#dormex.zz()
        
#####习题人际关系网格。
import socialnetwork
s = optimization.whatever(socialnetwork.domain, socialnetwork.crosscount)

print(s)
print(socialnetwork.crosscount(s))
socialnetwork.drawnetwork(s)
'''