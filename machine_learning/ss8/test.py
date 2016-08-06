import regression

from numpy import *
xArr,yArr=regression.loadDataSet('ex0.txt')

import matplotlib.pyplot as plt

'''
##标准算法
ws=regression.standRegres(xArr,yArr)
#print(xArr[:2])
print(ws)
xMat = mat(xArr)
yMat = mat(yArr)
yHat=xMat*ws

print(corrcoef(yHat.T,yMat))


fig = plt.figure()
ax=fig.add_subplot(111)
ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])

xCope=xMat.copy()
xCope.sort(0)
#print(xMat)
#print(xCope)
yHat=xCope*ws 
ax.plot(xCope[:,1],yHat)
plt.show()

###线性局部加强
#print(yArr[0])
#print(regression.lwlr(xArr[0],xArr,yArr,1.0))
#print(regression.lwlr(xArr[0],xArr,yArr,0.001))

yHat=regression.lwlrTest(xArr,xArr,yArr,0.003)
y2=regression.lwlrTest(xArr,xArr,yArr,0.1)
y3=regression.lwlrTest(xArr,xArr,yArr,1)##k值为10和k值为1没区别。k越小越精确
xMat = mat(xArr)
yMat = mat(yArr)

srtInd=xMat[:,1].argsort(0)
xSort=xMat[srtInd][:,0,:]###调用序列后升维，故采取该方法三维降成二维。

fig = plt.figure()
ax=fig.add_subplot(111)
ax.plot(xSort[:,1],yHat[srtInd],c='g')
ax.plot(xSort[:,1],y[srtInd],c='b')
#ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])

ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten().A[0],s=2,c='red')##此处y不能像plot中那样写法。
plt.show()

##鲍鱼预测
abX,abY=regression.loadDataSet('abalone.txt')
yHat01=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
yHat1=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
yHat10=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)

yHat01=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)##根据每个测试点在原来数据中找到预测值。
yHat1=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
yHat10=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)

a=regression.rssError(abY[100:199],yHat01.T)
b =regression.rssError(abY[100:199],yHat1.T)
c =regression.rssError(abY[100:199],yHat10.T)
print(a,b,c)

ws=regression.standRegres(abX[0:99],abY[0:99])
yHat=mat(abX[100:199])*ws
d=regression.rssError(abY[100:199],yHat.T.A)
print(d)


##岭回归
abX,abY=regression.loadDataSet('abalone.txt')
print(shape(abX))
#ridgeWeights=regression.ridgeTest(abX,abY)


fig = plt.figure()
ax=fig.add_subplot(111)
ax.plot(ridgeWeights)
plt.show()


##前向逐步
xArr,yArr=regression.loadDataSet('abalone.txt')
#print(regression.stageWise(xArr,yArr,0.1,20))

##最小二乘法比较
xMat = mat(xArr) 
yMat=mat(yArr).T
yMean = mean(yMat,0)
yMat = yMat - yMean     
xMat = regression.regularize(xMat)##数据标准化
weights=regression.standRegres(xMat,yMat.T)
print(weights.T)

'''
#乐高预测
lgX=[];lgY=[]
#regression.setDataCollect(lgX,lgY)
xArr,yArr=regression.loadDataSet('abalone.txt')
regression.crossValidation(xArr,yArr,10)
print()
#ridgeWeights=regression.ridgeTest(xArr,yArr)
#print(ridgeWeights)
print()
ws=regression.standRegres(xArr,yArr)
print(ws)




'''
##测试argsort()
a=matrix([0,3,5,1,2])
c=a.argsort()##二维矩阵中，argsort()和argsort(1)结果一致，即在同一行中，每一列数据比较大小；argsort(0)在同一列中，每行数字比较大小。
#xMat是200*1的矩阵，所以排列大小应当是在不同列同一位置比较，所以是argsort(0)
print(c)
#c=a.sort(0)
argsort(a) #按升序排列
argsort(-x) #按降序排列
x[argsort(x)] #通过索引值排序后的数组##x为np.array,如果是matrix，作为1*m型矩阵，应该是x[0,argsort(x)];如果是m*1型矩阵，则不变，但是结果会升一维。
#修正方法见xSort公式。

'''





