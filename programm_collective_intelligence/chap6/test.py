
import docclass

###最开始调用getwords进行单词计数的过程中，后来是如何标记每个词分在每一类的呢。

'''###贝叶斯之前 146页为止
c1= docclass.classifier(docclass.getwords)
#c1.train('the quick brown fox jumps over the quick lazy dog','good')
#c1.train('make quick money in the online casino','bad')
#print(c1.fcount('quick','good'))
#print(c1.fcount('quick','bad'))

docclass.sampletrain(c1)
#print(c1.fprob('quick','good'))
print(c1.weightedprob('money','good',c1.fprob))

docclass.sampletrain(c1)
print(c1.weightedprob('money','good',c1.fprob))


##ddd 贝叶斯  到150页结束
c1=docclass.naivebayes(docclass.getwords)
#docclass.sampletrain(c1)
#print(c1.prob('quick rabbit','good'))
#print(c1.prob('quick rabbit','bad'))

#print(c1.classify('owns water',default='unknown'))
#print(c1.classify('quick money',default='unknown'))

c1.setthreshold('bad',5.0)#这个后面的数字是设定出现多少次会被认为是符合‘bad’条件，而不是后续的‘unknown’
c1.setthreshold('good',4.0)
#print(c1.classify('owns water',default='unknown'))
for i in range(3):  
    docclass.sampletrain(c1)
    #print(i)
print(c1.classify('owns water',default='unknown'))

c1 = docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(c1)
print(c1.cprob('quick','good'))
#print(c1.cprob('quick','bad'))
#print(c1.cprob('money','bad'))
#print(c1.weightedprob('money','bad',c1.cprob))#cprob调用中也需要参数，怎么知道是默认把前面两个直接赋给它的呢？

print(c1.fisherprob('quick rabbit','good'))
print(c1.fisherprob('quick rabbit','bad'))


######对内容项进行归类。152页开始
c1 = docclass.fisherclassifier(docclass.getwords)
c1.setdb('test1.db')
docclass.sampletrain(c1)
#print(c1.classify('quick rabbit'))

#print(c1.classify('quick money'))
#c1.setminimum('bad',0.8)
#print(c1.classify('quick money'))
#c1.setminimum('good',0.8)
#print(c1.classify('quick money'))

c12=docclass.naivebayes(docclass.getwords)###这一段不太懂。之前c1.setdb是干嘛的。
c12.setdb('test1.db')
print(c12.classify('quick money'))

#####156页开始 
import feedfilter

c1 = docclass.fisherclassifier(docclass.getwords)
c1.setdb('python_feed.db')
feedfilter.read('python_search.xml',c1)#如何保证连续调用的呀。


###160 test
import feedfilter
c1=docclass.fisherclassifier(feedfilter.entryfeatures)
c1.setdb('python_feed.db')
feedfilter.read('python_search.xml',c1)



def kk():
    for i in range(4):
        print(i)
        if i+5>6: return i
    return i+1
    
    
a=kk()
print(a)'''


## 课后习题2
c2=docclass.naivebayes(docclass.getwords)

#docclass.sampletrain(c2)

c1=docclass.noignore(docclass.getwords)
#docclass.sampletrain(c2)
print('hhh')
#print(c2.prob('quick','good'))
#print(c1.prob('quick rabbit','bad'))
docclass.sampletrain(c1)
print(c1.prob('quick','good'))
#print(c1.prob('quick rabbit','bad'))

'''
#print(c1.classify('owns water',default='unknown'))
#print(c1.classify('quick money',default='unknown'))

c1.setthreshold('bad',5.0)#这个后面的数字是设定出现多少次会被认为是符合‘bad’条件，而不是后续的‘unknown’
c1.setthreshold('good',4.0)
#print(c1.classify('owns water',default='unknown'))
for i in range(3):  
    docclass.sampletrain(c1)
    #print(i)
print(c1.classify('water',default='unknown'))

c1 = docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(c1)
print(c1.cprob('quick','good'))
#print(c1.cprob('quick','bad'))
#print(c1.cprob('money','bad'))
#print(c1.weightedprob('money','bad',c1.cprob))#cprob调用中也需要参数，怎么知道是默认把前面两个直接赋给它的呢？

print(c1.fisherprob('quick rabbit','good'))
print(c1.fisherprob('quick rabbit','bad'))
'''