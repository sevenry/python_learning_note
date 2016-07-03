from numpy import *
import codecs
#引入codecs解决编码问题

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):#得到不重复全部单词
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):#根据所有词和一组词，得到该组词是否出现的0/1序列
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: 
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec

def trainNB0(trainMatrix,trainCategory):##输入各个类在总次数中的0/1分布和它们相对应的分类结果，得到计算的概率值。
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])#
    #print(numTrainDocs)
    #print(numWords)##32 不重复的单词项数
    pAbusive = sum(trainCategory)/float(numTrainDocs)##分类为侮辱类的结果占所有种类的比值
    #print(pAbusive)##0.5
    #p0Num = zeros(numWords); p1Num = zeros(numWords)      ##得到的结果每个单词的概率可能为0，影响连乘结果
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    
    #print(p0Num)
    #p0Denom = 0.0; p1Denom = 0.0                        #change to 2.0
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            #print(p1Num,'hh',p1Denom)
        else:
            p0Num += trainMatrix[i]###得到所有单词的重复总数序列
            p0Denom += sum(trainMatrix[i])##得到所有单词的个数
    #p1Vect = p1Num/p1Denom          #change to log()#侮辱文件中每个单词/侮辱文件总词汇的概率
    p1Vect = log(p1Num/p1Denom)#引入log解决连乘过小问题
    #print(p1Vect)
    #p0Vect = p0Num/p0Denom    #change to log()
    p0Vect = log(p0Num/p0Denom)  ##得到分为0类中的每个单词在总次数中出现的概率
    #print(p0Vect)
    return p0Vect,p1Vect,pAbusive

    ###
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #第一项是各个位置的单词出现的次数与相应的单词占总数的概率的乘积。
    ##本质是再与文件占总数的概率相乘，引入log便成了加法。
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    #print(p0)
    if p1 > p0:
        return 1
    else: 
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:##所有类中的每一类，而不是每个词
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))##得到测试组单词的0/1序列
    #print(thisDoc)
    print (testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print (testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb))

def bagOfWords2VecMN(vocabList, inputSet):##输入所有单词和一组词，得到0/1序列，1表示这组词在所有词中出现的位置。多次则为2/3等
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] 
    
def spamTest():
    docList=[]; classList = []; fullText =[]
    for i in range(1,7):
        r11=codecs.open('email/spam/%d.txt' % i)##_io.textIOwrapper
        try:
            rig=r11.read()##str格式
            #print(rig)
        except UnicodeDecodeError:
            print('email/spam/%d.txt' % i)
            raise
        #rig=r11.read()##str格式
        wordList = textParse(rig)
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        try:
            aa=codecs.open('email/ham/%d.txt' % i)##_io.textIOwrapper
            aa=aa.read()##编码有问题 我在这一行不能运行。
        except UnicodeDecodeError:
            print('email/spam/%d.txt' % i)
            raise
        #aa=open('email/ham/%d.txt' % i)##_io.textIOwrapper
        #aa=aa.read()##编码有问题
        wordList = textParse(aa)
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    #print(classList)#得到所有文件分别对应的1/0的分类，类似侮辱/非侮辱分类。
    #print(len(docList))
    vocabList = createVocabList(docList)#得到所有单词
    trainingSet = range(12); testSet=[]           #create test set
    trainingSet=list(trainingSet)##否则不能使用del
    #print(trainingSet)#0,1,2,...,49###12是可以读取的txt文件总数
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        #print(randIndex)##随机选取某个文件
        testSet.append(trainingSet[randIndex])
        #print(len(testSet))##得到选取的该文件得到测试集的序列号
        #print(testSet)
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:##剩下的作为训练集
        #print(docList[docIndex])
        #print(docIndex)##剩下的没有选择走的文件的编号，依旧是原有的编号，而非0,1,2的序列
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        #print(trainMat)
        trainClasses.append(classList[docIndex])
        #print(trainClasses)
    #print(len(trainMat),len(trainClasses))###长度相等
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:##判断分类结果
            errorCount += 1
            #print ("classification error",docList[docIndex])
    print ('the error rate is: ',float(errorCount)/len(testSet))

def calcMostFreq(vocabList,fullText):#得到全文中词汇组的计数
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True) 
    #python3中不使用iteritems，而是items
    return sortedFreq[:30]       

def localWords(feed1,feed0):
    import feedparser
    docList=[]; classList = []; fullText =[]
    #print(len(feed1['entries']),len(feed0['entries']))
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1) #NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)##sf is class 2 
    vocabList = createVocabList(docList)#create vocabulary
    top30Words = calcMostFreq(vocabList,fullText)   #remove top 30 words
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]           #create test set
    trainingSet=list(trainingSet)
    #print(len(trainingSet))
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print ('the error rate is: ',float(errorCount)/len(testSet))
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)[:10]##选择输出前十名
    print ("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**")
    for item in sortedSF:
        print (item[0])
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)[:10]
    print ("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**")
    for item in sortedNY:
        print (item[0])
















