from numpy import *
import adaboost

'''
datMat,classLabels=adaboost.loadSimpData()

#print(datMat[:,0])
#print( ones((shape(datMat)[0],1)))
D=mat(ones((5,1))/5)
#print(D)
#print(adaboost.buildStump(datMat,classLabels,D))
#adaboost.buildStump(datMat,classLabels,D)

classifierArray,kk=adaboost.adaBoostTrainDS(datMat,classLabels,44)
print(classifierArray)
#adaboost.addrin()

ans=adaboost.adaClassify(datMat,classifierArray)
#print(ans)

'''

datArr,labelArr=adaboost.loadDataSet('horseColicTraining2.txt')
classifierArray,aggClassEst=adaboost.adaBoostTrainDS(datArr,labelArr,40)
#print(classifierArray)
#print(aggClassEst[0:10])
#print(shape(aggClassEst.T))
#sortedIndicies = aggClassEst.T.argsort()
#print(shape(sortedIndicies))
#print(sortedIndicies[0,:10])
#print(sortedIndicies[0])
#print(len(classifierArray))
#adaboost.plotROC(aggClassEst.T,labelArr)

##利用测试集作检测
datatest,labeltest=adaboost.loadDataSet('horseColicTest2.txt')
pre=adaboost.adaClassify(datatest,classifierArray)
s=0
wrong=0
for i in range(len(pre)):
    s+=1
    if pre[i]!=labeltest[i]:
        wrong+=1
print(wrong/s)








