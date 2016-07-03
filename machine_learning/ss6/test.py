
#import svmMLiA
import svmkernel
from numpy import *

'''
dataArr,labelArr = svmkernel.loadDataSet('testSet.txt')
#print(labelArr)
#print(dataArr[:10])

#b,alphas=svmMLiA.smoSimple(dataArr, labelArr, 0.6, 0.001, 3)

b,alphas=svmkernel.smoP(dataArr,labelArr,0.6,0.001,40)
#print(b)
#print(alphas[alphas>0])
ws=svmkernel.calcWs(alphas,dataArr,labelArr)
#print(ws)

datMat=mat(dataArr)
for i in range(100):
    print(datMat[i]*mat(ws)+b)
    print(labelArr[i])
    print('hh')
    

svmkernel.testRbf()
'''
a=0
s=0
t=0
C=0
kTup=('rbf', 10)
for  count in range(10):
    s=0
    t=0
    for time in range(10):
        C=20*count+1
        a,b=svmkernel.testRbf(0.1,C)
        #kTup=('rbf', 0.1+0.2*count)
        #a,b=svmkernel.testDigits(C,kTup)
        s=s+a
        t=t+b
    print('the C is:',C)
    #print('the kTup is:',kTup)
    print('the train average:',s/10)
    print('the test average:',t/10)

    
'''
dataArr,labelArr = svmkernel.loadDataSet('testSetRBF.txt')
b,alphas = svmkernel.smoP(dataArr, labelArr, 200, 0.0001, 10000, ('rbf', 1.2)) #C=200 important
#print(b,alphas)
ws=svmkernel.calcWs(alphas,dataArr,labelArr)
#print(ws)
datMat=mat(dataArr); labelMat = mat(labelArr).transpose()
for i in range(20):
    print(datMat[i]*mat(ws)+b)
    print(labelArr[i])
    print('hh')
    
svmkernel.testDigits()'''