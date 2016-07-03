from numpy import *
import operator
from os import listdir

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
#调用该文件时，如果本身的数据和分类结果在同一个文件中，需要分为两部分分别赋给dataset和labels
    dataSetSize = dataSet.shape[0]
    #print(dataSetSize)#4
    #print(tile(inX,(dataSetSize,1)))##[[0,0],[0,0],[0,0],[0,0]]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    #print(diffMat)
    sqDiffMat = diffMat**2
    #print(sqDiffMat)
    sqDistances = sqDiffMat.sum(axis=1)
    #print(sqDistances)
    distances = sqDistances**0.5
    #print(distances)#[1.48,1.41,0,0.1]
    sortedDistIndicies = distances.argsort()  
    #print(sortedDistIndicies)#[2,3,1,0]
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        #print(voteIlabel)
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    #print(classCount)#这个不是返回距离最近的数，而是取跟它最接近的前k个数，然后分别统计结果
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    #这里把前k个数按照分类个数的多少排序，即分为‘1’类的如果最多，则在前面
    #print(sortedClassCount[0])
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    www=fr.readlines()
    numberOfLines = len(www)         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    #fr = open(filename)###如果省略www行，则需要添加这一行，参照源代码。but why？
    index = 0
    for line in www:
        line = line.strip()
        listFromLine = line.split('\t')
        #print(listFromLine)
        returnMat[index,:] = listFromLine[0:3]
        '''
        if listFromLine[-1]=='largeDoses':classLabelVector.append(3)
        else:
            if listFromLine[-1]=='smallDoses':classLabelVector.append(2)
            else:classLabelVector.append(1)'''
        classLabelVector.append(listFromLine[-1])#调用set文件时用这行不行，用上三行。望天。调用set2文件时用该行。
        index += 1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    #print(minVals)
    maxVals = dataSet.max(0)
    #print(maxVals)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]#行数。
    #print(m)#1000
    #print(len(dataSet))#1000
    #print(dataSet[1])
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals
 
def datingClassTest():
    hoRatio = 0.013      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    print(datingLabels[:20])
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)##测试综述
    errorCount = 0.0
    for i in range(numTestVecs):#其实是把所有数据分成两部分，一部分是test，一部分是train。
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],8)
        print ("the classifier came back with: %s, the real answer is: %s" % (classifierResult, datingLabels[i]))
        ##这里如果变成数字格式需要int()
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print ("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    print (errorCount)

def classifyPerson():
    resultList=['not','small','large']
    percentTats=float(input('percentage of time spent playing video games?'))
    ffmilise=float(input('miles per year?'))
    icecream=float(input('liters of ice cream per year?'))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals=autoNorm(datingDataMat)
    inArr=array([ffmilise,percentTats,icecream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print('you will like the one:', resultList[int(classifierResult)-1])

def img2vector(filename):#返回单行的数字
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):#32行
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect
    
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    #print(m)#1934
    trainingMat = zeros((m,1024))
    for i in range(m):
        
        fileNameStr = trainingFileList[i]
        #print(fileNameStr)
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])##前面的识别数字。
        #print(classNumStr)
        hwLabels.append(classNumStr)
        #print(hwLabels)#所有识别数字的顺序
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)#所有的单行数字为一个文件的总体
        #print(trainingMat)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)#得到每一个测试文件的单行文字
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 5)
        #它之前没有把得到的每个单行文字和识别的数字建立联系，但是它安装同样的顺序放置，所以依旧可以据此进行判别。
        #print ("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print ("\nthe total number of errors is: %d" % errorCount)
    print ("\nthe total error rate is: %f" % (errorCount/float(mTest)))












