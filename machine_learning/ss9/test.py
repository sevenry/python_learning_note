
from numpy import *

import regTrees

'''
testMat=mat(eye(4))
#print(testMat)

myDat=regTrees.loadDataSet('ex00.txt')
myMat=mat(myDat)

#print(myMat[55,0],myMat[41,0],myMat[39,0])
#mat0, mat1 = regTrees.binSplitDataSet(myMat,0,myMat[55,0])

#print(mat0,mat1)

#regTrees.regLeaf(myMat)

#regTrees.createTree(myMat)

myDat1=regTrees.loadDataSet('ex2.txt')
myMat1=mat(myDat1)
mytree=regTrees.createTree(myMat1, ops=(0,40))
print(mytree)

myDatTest=regTrees.loadDataSet('ex2test.txt')
myDat2Test=mat(myDatTest)
#newTree=regTrees.prune(mytree,myDat2Test)
myDat2Test=[]
newTree=regTrees.prune(mytree,myDat2Test)

print(newTree)

##175
myMat2 = mat(regTrees.loadDataSet('exp2.txt'))
tree = regTrees.createTree(myMat2, regTrees.modelLeaf, regTrees.modelErr, (1,10))
print(tree)
'''

#178
##回归树预测
trainMat = mat(regTrees.loadDataSet('bikeSpeedVsIq_train.txt'))
testMat = mat(regTrees.loadDataSet('bikeSpeedVsIq_test.txt'))
#myTree = regTrees.createTree(trainMat, ops=(1,20))
#yHat = regTrees.createForeCast(myTree, testMat[:,0])
#a = corrcoef(yHat, testMat[:,1], rowvar=0)[0,1]

##利用模型树来预测
#moxingTree = regTrees.createTree(trainMat, regTrees.modelLeaf, regTrees.modelErr, (1,20))
#yHat2 = regTrees.createForeCast(moxingTree, testMat[:,0], modelEval = regTrees.modelTreeEval)
#a = corrcoef(yHat2, testMat[:,1], rowvar=0)[0,1]

#print(a)

##标准线性回归方法
ws, X, Y = regTrees.linearSolve(trainMat)
m=len(testMat)
yHat = mat(zeros((m,1)))
    
for i in range(m):
    yHat[i] = testMat[i,0]*ws[1,0]+ws[0,0]
    
c=corrcoef(yHat, testMat[:,1], rowvar=0)[0,1]
print(c)

'''
#测试range

for i in range(3):
    print(i)
    '''
 







