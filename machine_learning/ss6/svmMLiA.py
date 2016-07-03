import codecs
from numpy import *
from time import sleep

def loadDataSet(fileName):
    dataMat = []; labelMat = []
    fr = codecs.open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    j=i #we want to select any J not equal to i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj > H: 
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    #print(len)#100
    #print(len(labelMat))#100
    b = 0; m,n = shape(dataMatrix)#100,2
    alphas = mat(zeros((m,1)))
    iter = 0
    while (iter < maxIter):
        #print('lalala')
        alphaPairsChanged = 0
        for i in range(5):
            #print(i,'time')
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b##预测的结果，参看公式7.29
            #alphas,labelMat是100*1的矩阵，dataMatrix是100*2的矩阵，dataMatrix[i,:].T是2*1的矩阵，最后是数值
            Ei = fXi - float(labelMat[i])##误差
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)##选取了100以内的一个随机数
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy();
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H:#print ("L==H"); 
                    continue
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                ##用于调整alphas[j]的值，只考虑小于0的情况。
                if eta >= 0: #print ("eta>=0"); 
                    continue
                ##后续为逐步调整alphas[i]和alphas[j]的情况，保证为正。
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] - alphaJold) < 0.00001): #print ("j not moving enough"); 
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                #参看公式7.33,7.34
                alphaPairsChanged += 1
                #print(alphaPairsChanged,'why')
                print ("iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
        if (alphaPairsChanged == 0): iter += 1
        ##没有改变的情况下，iter值增加；maxIter次增加后则退出大循环。即优化至无法优化的时候退出循环。
        else: iter = 0###改变了iter值仍为0；
        #print(iter,'jjjj')
        print ("iteration number: %d" % iter)
    return b,alphas

class optStruct:
    def __init__(self,dataMatIn, classLabels, C, toler):  # Initialize the structure with the parameters 
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2))) ##变成了m*2的矩阵，第一项为标志位，第二项为误差值。
        #self.K = mat(zeros((self.m,self.m)))
        #for i in range(self.m):
            #self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)

def calcEk(oS, k):##返回误差值
    fXk = float(multiply(oS.alphas,oS.labelMat).T*oS.X*oS.X[k,:].T + oS.b)
    Ek = fXk - float(oS.labelMat[k])
    return Ek
        
def selectJ(i, oS, Ei):         
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1,Ei]  
    #aaa=nonzero(oS.eCache[:,0].A)
    #print(len(aaa))#2
    validEcacheList = nonzero(oS.eCache[:,0].A)[0]##后缀A是把matrix变成array
    ##nonzero的第一项是非零项的序列号，第二项是在该项中的位置
    ##此处nonzero的对象中的每一项都只有一个数字，所以此处得到的第二项均为0，故不需要。
    #print(validEcacheList)
    #print(oS.eCache)
    #print(oS.eCache[:,0])
    #print(oS.eCache[:,0].A)
    #print(nonzero(oS.eCache[:,0].A))
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:   #通过循环的方式得到最大的k，不像smoSimple中是随机数得到j来计算。
            if k == i: continue 
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return maxK, Ej
    else:   #in this case (first time around) we don't have any valid eCache values
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
    return j, Ej

def updateEk(oS, k):#
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1,Ek]

def innerL(i, oS):#该函数本身内部不做循环，只做是否修改了alphas值的计数用
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
    #需要修正i项，所以调用selectJ函数，将i的标记位改成1
        j,Ej = selectJ(i, oS, Ei) #等同于smoSimple 中的selectJrand 方法。
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy();
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L==H: #print ("L==H"); 
            return 0
        eta=2.0*oS.X[i,:]*oS.X[j,:].T-oS.X[i,:]*oS.X[i,:].T-oS.X[j,:]*oS.X[j,:].T
        #eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j] #changed for kernel
        if eta >= 0: #print ("eta>=0"); 
            return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei - Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
        ##alphas值进行了修改，calcEK中的fXk值变化，且只影响j项的fXk值，所以Ej值相应的改变，所以需要更新误差。
        updateEk(oS, j) #更新误差值
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): 
            #print ("j not moving enough"); 
            return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j])
        updateEk(oS, i)#同理更新i的值。
        b1 = oS.b - Ei- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i,:]*oS.X[i,:].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[i,:]*oS.X[j,:].T
        b2 = oS.b - Ej- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i,:]*oS.X[j,:].T- oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[j,:]*oS.X[j,:].T
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2)/2.0
        return 1
    else: return 0

def smoP(dataMatIn, classLabels, C, toler, maxIter,kTup=('lin', 0)):    #full Platt SMO
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler)
    #print(oS.m)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        #print('hh')#测试循环
        alphaPairsChanged = 0
        if entireSet:   #go over all
            #print('所有')
            for i in range(oS.m):
                
                alphaPairsChanged += innerL(i,oS)
                #print ("fullSet, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
            iter += 1
        else:#go over non-bound (railed) alphas
            nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0] 
            #print(len(nonBoundIs),'边界')
            for i in nonBoundIs:#遍历所有的非边界值
                alphaPairsChanged += innerL(i,oS)
                #print ("non-bound, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
            iter += 1
        #print('alphas',alphaPairsChanged)
        if entireSet: entireSet = False #如果执行了所有，且值有改变则需要执行边界，如果执行了所以值没有改变，退出。
        elif (alphaPairsChanged == 0): entireSet = True  #如果执行边没有改变，则执行所有。如果执行边界有改变，则继续边界
        #所以该算法一定是执行所有并满足才停止。
        #print(iter, entireSet)
        #print ("iteration number: %d" % iter)
    return oS.b,oS.alphas

def calcWs(alphas,dataArr,classLabels):###得到w
    X = mat(dataArr); labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w




 

























