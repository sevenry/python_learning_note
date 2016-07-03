
from math import log
import operator

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        #print(labelCounts.keys())
        if currentLabel not in labelCounts.keys():
            #print('hhh',currentLabel)
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
       # print(labelCounts[currentLabel])
    shannonEnt = 0.0
    #print(labelCounts)
    for key in labelCounts:
        #print(key)
        #print(labelCounts[key])
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt

def splitDataSet(dataSet, axis, value):#根据某个特征项的取值value，得到数据中符合条件的这些。
    retDataSet = []
    for featVec in dataSet:
        #print(featVec[axis])
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            #print(reducedFeatVec)
            reducedFeatVec.extend(featVec[axis+1:])
            #print(reducedFeatVec)
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):##一组数据有n个特特征，选出信息增益最大的特征项。
    numFeatures = len(dataSet[0]) - 1     #有n个特征项得到n值
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #iterate over all the features
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        #print(featList)
        uniqueVals = set(featList)       #get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     #信息增益，是指在原来基础上降低的熵值，越高越好。
        #print(infoGain)
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
    return bestFeature                      #returns an integer

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    #print(classList)
    if classList.count(classList[0]) == len(classList): 
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    #print(myTree)
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]#得到该组数据中最佳特征项该项的值
    #print(featValues)
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        #print(subLabels)
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
        ##传入的dataset已经是按照当前最佳特征项的几个值分得的结果
    
    return myTree                            

def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    print(firstStr)
    secondDict = inputTree[firstStr]
    print(secondDict)
    featIndex = featLabels.index(firstStr)
    print(featIndex)
    key = testVec[featIndex]
    print(key)
    valueOfFeat = secondDict[key]
    print(valueOfFeat)
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel










