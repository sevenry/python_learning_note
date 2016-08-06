
from numpy import *

def loadDataSet(fileName):      
    numFeat = len(open(fileName).readline().split('\t')) - 1 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print ("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T*yMat)###最小二乘法求回归系数的计算公式。
    return ws
    
def lwlr(testPoint,xArr,yArr,k=1.0):##对每个点进行局部加强算法，k=1时线性平滑；k值越小越尽可能的拟合所有点。
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):                     
        diffMat = testPoint - xMat[j,:]     
        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print ("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))##局部加权线性回归函数计算
    ###此时ws不是常规的k和b两项，认为结果由多组影响因素线性和组成
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):  #对一组测试点在原数据中用局部加强给出预测值。如果测试点在原数据中，较准确。
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

def rssError(yArr,yHatArr):#返回多项误差平方总和
    return ((yArr-yHatArr)**2).sum()

def ridgeRegres(xMat,yMat,lam=0.2):##lam可以视作惩罚函数，越小对原矩阵影响越小。
    xTx = xMat.T*xMat
    #print(shape(xTx))##8,8
    denom = xTx + eye(shape(xMat)[1])*lam
    #print(shape(denom))
    if linalg.det(denom) == 0.0:
        print ("This matrix is singular, cannot do inverse")
        return
    ws = denom.I * (xMat.T*yMat)
    #print(ws)
    return ws
    
def ridgeTest(xArr,yArr):##根据传入的特征项和结果，生成一系列惩罚函数不同的ws。
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean     
    xMeans = mean(xMat,0)   
    xVar = var(xMat,0)     
    xMat = (xMat - xMeans)/xVar
    numTestPts = 30##这与后面的crossValidation测试30次吻合。
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))##生成不同的lam值对应的ws
        wMat[i,:]=ws.T
    return wMat
    
def regularize(xMat):
    inMat = xMat.copy()
    inMeans = mean(inMat,0)  
    #print(inMeans)
    inVar = var(inMat,0)      
    #print(inVar)
    inMat = (inMat - inMeans)/inVar
    #print(inMat[0])
    return inMat

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean     
    xMat = regularize(xMat)##数据标准化
    m,n=shape(xMat)
    returnMat = zeros ((numIt, n))
    ws = zeros((n,1)); wsTest = ws.copy(); wsMax = ws.copy()
    for i in range(numIt):
        #print (ws.T)##这里的第一行不出现在最后结果中，结果的最后一行这里也没有出现。所以导致二者最后一行不同。
        lowestError = inf; 
        #print(lowestError)#无限大。
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps*sign
                yTest = xMat*wsTest
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i, :] = ws.T
    return returnMat


from time import sleep
import json
import urllib.request
def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
    sleep(10)
    myAPIstr = 'AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
    pg = urllib.request.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem = retDict['items'][i]
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else: newFlag = 0
            listOfInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if  sellingPrice > origPrc * 0.5:
                    print ("%d\t%d\t%d\t%f\t%f" % (yr,numPce,newFlag,origPrc, sellingPrice))
                    retX.append([yr, numPce, newFlag, origPrc])
                    retY.append(sellingPrice)
        except: print ('problem with item %d' % i)
    
def setDataCollect(retX, retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)

def crossValidation(xArr,yArr,numVal=10):
    m = len(yArr)                           
    indexList = range(m)
    indexList = list(indexList)#python3要先存成list
    errorMat = zeros((numVal,30))#create error mat 30columns numVal rows
    for i in range(numVal):##对同样的数据分成多次不同的测试组和训练组。
        trainX=[]; trainY=[]
        testX = []; testY = []
        random.shuffle(indexList)
        for j in range(m):#create training set based on first 90% of values in indexList
            if j < m*0.9: 
                trainX.append(xArr[indexList[j]])
                trainY.append(yArr[indexList[j]])
            else:
                testX.append(xArr[indexList[j]])
                testY.append(yArr[indexList[j]])
        wMat = ridgeTest(trainX,trainY)    ##生成30组ws的值。
        #print(shape(wMat))
        #print(wMat)
        for k in range(30):#对30组不同的ws值进行比对。最好改成：for k in range(len(wMat))
            matTestX = mat(testX); matTrainX=mat(trainX)
            #print(shape(matTestX))
            #print(shape(mat(wMat[k,:])))
            #print(shape(trainY))
            #xxx=regularize(matTrainX)#直接调用函数求规格化。
            meanTrain = mean(matTrainX,0)##求得各特征项平均值。
            varTrain = var(matTrainX,0)
            matTestX = (matTestX-meanTrain)/varTrain ##用训练的参数将测试集标准化。不能直接对测试数据调用标准化函数。
            yEst = matTestX * mat(wMat[k,:]).T + mean(trainY)#测试岭函数结果。因为岭函数中有标准化，所以测试时需要对测试数据同样方式标准化。
            errorMat[i,k]=rssError(yEst.T.A,array(testY))
            #print errorMat[i,k]
    meanErrors = mean(errorMat,0)##求均值，即不同分类同一k值求得误差平均。
    minMean = float(min(meanErrors))
    bestWeights = wMat[nonzero(meanErrors==minMean)]
    xMat = mat(xArr); yMat=mat(yArr).T
    meanX = mean(xMat,0); varX = var(xMat,0)
    unReg = bestWeights/varX##将数据还原成标准化输出。这里的ws是乘以每个标准化单位数值的，即ws*(x-xmean)/varX=y-ymean
    print ("the best model from Ridge Regression is:\n",unReg)
    print ("with constant term: ",-1*sum(multiply(meanX,unReg)) + mean(yMat))





















