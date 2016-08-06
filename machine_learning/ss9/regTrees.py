
from numpy import *

def loadDataSet(fileName):       
    dataMat = []                 
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float,curLine))#python3
        dataMat.append(fltLine)
    return dataMat
       
def binSplitDataSet(dataSet, feature, value):##输入数组，所在维度，具体数值，据此将数据分成两组
    #mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]###某行对应位置高于value的所有行中，输出第一行。
    #mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]###如果某行对应位置低于value，输出符合条件的第一行。
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:]#依后文在chooseBestSplit函数中的应用，似乎应当输出所有符合条件的行数。
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:]
    return mat0,mat1

def regLeaf(dataSet):##返回矩阵最后一列均值
    return mean(dataSet[:,-1])

def regErr(dataSet):#返回矩阵最后一列各个数据与平均值差值平方之和
    return var(dataSet[:,-1]) * shape(dataSet)[0]
    
def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):#根据数据，建立树，进行分枝。
###通过修改ops改变剪枝方法，预剪枝。
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat == None: return val #说明仅一个数据，或者继续分组无意义
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)#调用函数根据结果将当前数据分成两组，继续分组。
    retTree['left'] = createTree(lSet, leafType, errType, ops)#如果最后left和right仅为数值的话，即为分组数据输出结果均值。
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    #print(retTree)
    return retTree  

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
##根据输入数据，找到最佳分界点。返回最佳分界点所在维度，即哪一项，和具体数值
#ops第一项作为分组后结果与不分组结果差值比较限值，即在该范围内认为不继续分组；第二项是根据分组结果后每一组个数，少于该数目则认为不继续分组。
    tolS = ops[0]; tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:#只有一个数据返回本身
        return None, leafType(dataSet)
    m,n = shape(dataSet)
    S = errType(dataSet)#全局平方和
    bestS = inf; bestIndex = 0; bestValue = 0
    #print(n)#2
    for featIndex in range(n-1):
        '''
        dat=[]
        #print(featIndex)
        for k in range(len(dataSet)):
            dat.append(dataSet[k,featIndex])
        for splitVal in set(dat):###改写法1
        #for splitVal in set(dataSet[:,featIndex]):###python3中跑不通。'''
        dat=dataSet[:,featIndex].T.tolist()[0]
        for splitVal in set(dat):##改写法2
            if splitVal<max(dat) and splitVal>min(dat):###这一行需要加上否则无法调用binSplitDataSet函数。
                mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
                if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue##分得结果中某一组内数据过少则不参与比较
                newS = errType(mat0) + errType(mat1)##分组后各自的平方和
                if newS < bestS: 
                    bestIndex = featIndex
                    bestValue = splitVal
                    bestS = newS
    if (S - bestS) < tolS:#意味分组并不理想
        return None, leafType(dataSet) 
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): #
        return None, leafType(dataSet)
    return bestIndex,bestValue

def isTree(obj):##判断是否为字典，即此处是否有分枝
    return (type(obj).__name__=='dict')

def getMean(tree):#从叶节点开始，层层上传得到根部的值。每一枝节点都是下一层两个枝/叶节点的均值。
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    print(tree['left'],tree['right'])
    return (tree['left']+tree['right'])/2.0
    
def prune(tree, testData):
    if shape(testData)[0] == 0: return getMean(tree) #测试集为空，不改变
    if (isTree(tree['right']) or isTree(tree['left'])):#有一枝为枝节点时
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    if isTree(tree['left']): tree['left'] = prune(tree['left'], lSet)
    if isTree(tree['right']): tree['right'] =  prune(tree['right'], rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):##均为叶节点时
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])##将数据分为左右两部分
        errorNoMerge = sum(power(lSet[:,-1] - tree['left'],2)) +\
            sum(power(rSet[:,-1] - tree['right'],2))##分别两部分与左右值的差值平方和
        treeMean = (tree['left']+tree['right'])/2.0
        errorMerge = sum(power(testData[:,-1] - treeMean,2))#所有数据与左右均值的差值平方和
        if errorMerge < errorNoMerge: 
            print ("merging")
            return treeMean
        else: return tree
    else: return tree

def linearSolve(dataSet):##将数据集的输入和输出线性回归化
    m,n = shape(dataSet)
    X = mat(ones((m,n))); Y = mat(ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1]; Y = dataSet[:,-1]
    xTx = X.T*X
    if linalg.det(xTx) == 0.0:
        raise NameError('this matrix is singular, cannot do inverse, try increasing the second value of ops')
    ws = xTx.I*(X.T * Y)
    return ws,X,Y
    
def modelLeaf(dataSet):#输出数据的线性关系值;
#这样在createTree中调用该方法，则返回的树的left和right就是ws的数值，即以线性划分：某些数据在线性关系1上，某些数据在线性关系2上
    ws,X,Y = linearSolve(dataSet)
    return ws 
  
def modelErr(dataSet):#输出根据线性关系得到的预测值和实际值的差值平方和
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y-yHat, 2))
    
def regTreeEval(model, inDat):
    return float(model)

def modelTreeEval(model, inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

def treeForeCast(tree, inData, modelEval=regTreeEval):
    if not isTree(tree): return modelEval(tree, inData)##如果非树节点，返回该点数值
    if inData[tree['spInd']] > tree['spVal']:##测试点数值高于分界值，划分到left 继续递归。分为left是因为binSplitDataSet设定left为高于临界值。
        if isTree(tree['left']): return treeForeCast(tree['left'], inData, modelEval)
        else: return modelEval(tree['left'], inData)
    else:
        if isTree(tree['right']): return treeForeCast(tree['right'], inData, modelEval)
        else: return modelEval(tree['right'], inData)
        
def createForeCast(tree, testData, modelEval=regTreeEval):
    m=len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0] = treeForeCast(tree, mat(testData[i]), modelEval)
    return yHat



























