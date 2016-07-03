from numpy import *


def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])#生成每一新的行，每一行有三个数
        labelMat.append(int(lineArr[2]))#在原来的行中加一个数
    return dataMat,labelMat
 
def sigmoid(inX):
    return 1/(1+exp(-inX)) ##对应y=1的概率
    ###目标函数，根据此处选择是使用梯度上升还是梯度下降。

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)             #convert to NumPy matrix
    labelMat = mat(classLabels).transpose() #convert to NumPy matrix
    m,n = shape(dataMatrix)
    #print(m,n)
    a,b=shape(labelMat)
    #print(a,b)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    #print(weights)
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
        #print(weights)
    return weights

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    #weights=wei.getA()#如果参数wei是matrix，将它转为ndarray
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        #print(i)
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')#画出具体的颜色点
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)#numpy.ndarray
    #print(x)
    k=len(x)
    y = (-weights[0]-weights[1]*x)/weights[2]##生成matrix；ipython里是数组，不用变换
    ##如果weights[0]是具体的数值，比如3，则仍旧是数组；与变量进行计算生成矩阵
    y=array(y).reshape(k)#这里将(1,60)的二维矩阵转化为数组再转化为60项的一维数组
    #print(y)
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   #initialize to all ones
    for j in range(177):
        for i in range(m):#对这一系列值，每个值进行一次调整
            h = sigmoid(sum(dataMatrix[i]*weights))#weights中有三项，为array。
            error = classLabels[i] - h
        
            weights = weights + alpha * error * dataMatrix[i]
        #print(weights)
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=10):
    m,n = shape(dataMatrix)
    weights = ones(n)   #initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        dataIndex=list(dataIndex)#range不支持删除
        #print(dataIndex[3])
        for i in range(4):
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not 
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            #print(randIndex)
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            #print(h)##验证sigmoid是当做分类函数使用，值为0或1，可以认为只有分类出错才存在error的统计。
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 500)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print ("the error rate of this test is: %f" % errorRate)
    return errorRate

def multiTest():
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest()
    print ("after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests)))
        

















