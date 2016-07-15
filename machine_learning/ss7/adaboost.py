

from numpy import *

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels
 
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#利用分类判据得到判断结果
##利用传入的参量dimen选择不同的位置，threshVal选择位置上分界线数字的值，threshIneq来选择该位置上大或者小的判断方式
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

def buildStump(dataArr,classLabels,D):#根据输入的权重得到对一系列数据取得最佳特征组和判断值界限。
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
    minError = inf 
    for i in range(n):##每一项的数字个数。即在每一项中选择不同位置的数字作为判别项。
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();##同样位置的最值。
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            #print(i,j)
            for inequal in ['lt', 'gt']: 
                threshVal = (rangeMin + float(j) * stepSize)###逐步调整判断值的大小。
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T*errArr#由于D设置为1/m，所以全错值为1，全对值为0，可视为误差的百分比。 
                if weightedError < minError:##得到最佳的分类方式
                    #print(errArr)
                    
                    #print(weightedError)
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst

def adaBoostTrainDS(dataArr,classLabels,numIt=40):##每次调用buildStump函数后修改权重，再次迭代，给出多组简单分类器，使得最终误差为0.
###关于参数，如果有给默认值，那么调用时可以缺省，如果没有给默认值，则调用时需输入参数值
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)   
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#随着反复迭代，每一次迭代获得一个简单分类器
        #print('D:',D.T)
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))#α的计算公式，是根据已经得到的分类器计算出的权重，所以作为该分类器的系数，而非下一次计算的系数。
        #print(alpha)
        bestStump['alpha'] = alpha  
        #print(bestStump)
        weakClassArr.append(bestStump)               
        #print('classEst:',classEst.T)
        expon = multiply(-1*alpha*mat(classLabels).T,classEst)##如果二者相同，对应数值为负，反之为正。在D更新中负值将比例系数降低，正则加大误分类权重
        #print(expon)
        D = multiply(D,exp(expon))#在上一循环基础上更新权值。         
        #print(D)
        D = D/D.sum()##通过该方法修改D的权重，不再为等权重的方法
        aggClassEst += alpha*classEst #最终实现该行正负与分类一致。为多个分类器的和。
        #print('aggClassEst:',aggClassEst)
        #print(sign(aggClassEst) != mat(classLabels).T)##aggclassEst的正负与classLabels一致，则此时!=的判断为False
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))##True为1，False为0，
        #print(aggErrors)
        errorRate = aggErrors.sum()/m##分类器之和的误差。
        #print ("total error: ",errorRate)
        if errorRate == 0.0: break
    return weakClassArr,aggClassEst##前者为具体的分类器的判断标准，后者为每一分类器的分类结果。

def adaClassify(datToClass,classifierArr):##给出一组数据，综合所得到的简单分类器，利用分类判据，预测结果。
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):#每一次循环使用一组新的分类器。
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])
        #print(classEst)
        aggClassEst += classifierArr[i]['alpha']*classEst
        #print (aggClassEst)
    return sign(aggClassEst)

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def plotROC(predStrengths, classLabels):
    import matplotlib.pyplot as plt
    cur = (1.0,1.0) 
    ySum = 0.0 #variable to calculate AUC
    numPosClas = sum(array(classLabels)==1.0)
    yStep = 1/float(numPosClas); xStep = 1/float(len(classLabels)-numPosClas)
    sortedIndicies = predStrengths.argsort()#按数值排序给出索引##本身是matrix
    #print(sortedIndicies)
    
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    #loop through all the values, drawing a line segment at each point
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delX = 0; delY = yStep;
        else:
            delX = xStep; delY = 0;
            ySum += cur[1]
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')
        cur = (cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
    plt.title('ROC curve for AdaBoost horse colic detection system')
    ax.axis([0,1,0,1])
    plt.show()
    print ("the Area Under the Curve is: ",ySum*xStep)













def addrin(k=4):##验证参数缺省。
    s=0
    for i in range(k):
        s+=k
    return s 
























