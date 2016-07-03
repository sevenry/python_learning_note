from numpy import *

import bayes
import feedparser

'''
listposts,listclasses=bayes.loadDataSet()
myVocablist=bayes.createVocabList(listposts)
#print(myVocablist)

aa=bayes.setOfWords2Vec(myVocablist,listposts[0])
bb=bayes.setOfWords2Vec(myVocablist,listposts[2])
#print(aa)
#print(bb)

trainMat=[]
for postinDoc in listposts:
    trainMat.append(bayes.setOfWords2Vec(myVocablist,postinDoc))

#print(trainMat)
#print(listclasses)
p0v,p1v,pab=bayes.trainNB0(trainMat,listclasses)
#rint(p0v)
#bayes.testingNB()

mysent='This book is the best book on Python on M.L. I have ever laid eyes upon.'
tww=mysent.split()
#print(tww)

import re
regEx = re.compile('\\W*')
listOfTokens = regEx.split(mysent)
#print(listOfTokens)
#print([tok for tok in listOfTokens if len(tok)>0])

emailText = open('email/ham/6.txt').read()
listOfTokens=regEx.split(emailText)
'''

#bayes.spamTest()
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
#print(ny)
#vocabList,pSF,pNY=bayes.localWords(ny,sf)
#vocabList,pSF,pNY=bayes.localWords(ny,sf)
bayes.getTopWords(ny,sf)













