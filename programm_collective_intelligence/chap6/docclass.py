import re
import math
from sqlite3 import dbapi2 as sqlite

def sampletrain(cl):#集中处理一堆语句的train
  cl.train('nobody owns the water.','good')
  cl.train('the quick rabbit jumps fences','good')
  cl.train('buy pharmaceuticlas now','bad')
  cl.train('make quick money at the online casino','bad')
  cl.train('the quick brown fox jumps','good')

def getwords(doc):
  splitter=re.compile('\\W*')
  #print (doc)
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  return dict([(w,1) for w in words])
  
class classifier:
  def __init__(self,getfeatures,filename=None):
    self.fc={}
    self.cc={}
    self.getfeatures=getfeatures
    #print(getfeatures)#这一行通常接受的是item，即搜索的词组，结果如 quick:1;rabbit:1
    
  ###之前的用法
  def incf(self,f,cat):#对每一个单词分别出现在不同的cat里进行总共计数，如：'now':{'good':1}
    self.fc.setdefault(f,{})
    self.fc[f].setdefault(cat,0)
    self.fc[f][cat]+=1
    
  def incc(self,cat):
    self.cc.setdefault(cat,0)
    self.cc[cat]+=1
    
  def fcount(self,f,cat):#通过incf中的定义完成计数。但是不能应用于交集的计算。
    #print(self.fc)
    if f in self.fc and cat in self.fc[f]:     
      return float(self.fc[f][cat])
    return 0.0
    
  def catcount(self,cat):
    #print(self.cc)
    #print(float(self.cc[cat]))
    if cat in self.cc:
      return float(self.cc[cat])
    
    return 0
  
  def totalcount(self):
    return sum(self.cc.values())
    
  def categories(self):
    return self.cc.keys()
  
  '''
  
  ###154页之后的函数
  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      self.con.execute("insert into fc values ('%s','%s',1)" 
                       % (f,cat))
    else:
      self.con.execute(
        "update fc set count=%d where feature='%s' and category='%s'" 
        % (count+1,f,cat)) 
  
  def fcount(self,f,cat):
    res=self.con.execute(
      'select count from fc where feature="%s" and category="%s"'
      %(f,cat)).fetchone()
    if res==None: return 0
    else: return float(res[0])

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      self.con.execute("insert into cc values ('%s',1)" % (cat))
    else:
      self.con.execute("update cc set count=%d where category='%s'" 
                       % (count+1,cat))    

  def catcount(self,cat):
    res=self.con.execute('select count from cc where category="%s"'
                         %(cat)).fetchone()
    if res==None: return 0
    else: return float(res[0])
  
  def categories(self):
    cur=self.con.execute('select category from cc');
    return [d[0] for d in cur]
  
  
  def totalcount(self):
    res=self.con.execute('select sum(count) from cc').fetchone();
    if res==None: return 0
    return res[0]

    '''
    
  def train(self,item,cat):
    features = self.getfeatures(item)
    for f in features:
      self.incf(f,cat)
      
    self.incc(cat)
    #self.con.commit()###154页之后的函数
  
  def fprob(self,f,cat):
    if self.catcount(cat)==0:return 0
    #print(self.fcount(f,cat),f,cat)
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    basicprob=prf(f,cat)
    #print(basicprob)
    totals=sum([self.fcount(f,c) for c in self.categories()])
    #print(totals)

    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp
    
  def setdb(self,dbfile):
    self.con=sqlite.connect(dbfile)    
    self.con.execute('create table if not exists fc(feature,category,count)')
    self.con.execute('create table if not exists cc(category,count)')


class naivebayes(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)#对查找的关键词出现在每个cat中进行计数。   
    p=1
    #print(features)
    for f in features: 
      #print(f,self.weightedprob(f,cat,self.fprob))
      p = p * self.weightedprob(f,cat,self.fprob)
      #print(p)
    return p

  def prob(self,item,cat):
    #print(self.totalcount())
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    #print(self.thresholds)
    if cat not in self.thresholds: return 1.0#如果不设置setthreshold中的值，此时为空，所以返回1.0
    #print(self.thresholds[cat])
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    print('happy')
    probs={}
    max=0.0
    #print(self.categories())
    for cat in self.categories():#循环比较找到搜索词条中更优势的cat一方。
      
      probs[cat]=self.prob(item,cat)
      #print(probs[cat],cat)
      if probs[cat]>max: 
        max=probs[cat]
        #print(max)
        best=cat
        
    #print(best,'\n')

    for cat in probs:
      #print(cat)
      #print(self.getthreshold(best))
      if cat==best: continue#符合条件绕过后续内容。不符合才继续。
      #print('hhh',cat)
      #print(probs[cat],cat)
      if probs[cat]*self.getthreshold(best)>probs[best]: return default#如果满足if语句执行了return行，则跳出for循环。
      #如果good是best，这就是bad的prob值乘以getthreshold(good)值大于 good的prob值，返回unknown。
      
    #print(probs[best],best)
    return best

class fisherclassifier(classifier):
  def cprob(self,f,cat):
    clf=self.fprob(f,cat)
    #print(clf)
    if clf==0: return 0

    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    p=clf/(freqsum)
    return p
    
  
  def fisherprob(self,item,cat):
    p=1
    features=self.getfeatures(item)
    #print(features)#'quick':1 ,'rabbit',1
    for f in features:
      #print(self.cprob)
      p*=(self.weightedprob(f,cat,self.cprob))

    fscore=-2*math.log(p)

    return self.invchi2(fscore,len(features)*2)
    
  def invchi2(self,chi, df):#倒置对数卡方函数是个什么鬼
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)
    
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}

  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]
    
  def classify(self,item,default=None):
    print('mygod')
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      print(c,p)
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
      print(best)
    return best
    

class noignore(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)#对查找的关键词出现在每个cat中进行计数。   
    p=1
    #print(features)
    for f in features: 
      #print('doc',f,self.fprob(f,cat))
      p = p * self.fprob(f,cat)#此处其实不符合贝叶斯公式，应该是item中所有元素出现在cat类别中的个数除以cat的总个数，不应该视为独立事件互相叠加。
    return p
  
  def why(self,item,cat):
    features=self.getfeatures(item)
    for f in features:
      print(self.fcount(f,cat))
    return 1
  
  def strprob(self,item):#这个函数只能解决item为单一的问题。重点是在如何完成求交集的函数。
    features=self.getfeatures(item)
    p=1
    #print(features)
    totals=self.totalcount()
    #print(totals)
    
    for f in features:
      ff=sum([self.fcount(f,c) for c in self.categories()])/totals
      p=p * ff#这一行的函数其实不对，应该是求得item中所有元素同时出现的个数/totals就可以了。
      #print('str',f,ff)
    if p==0:return 1
    #print(p)
    return p
  
  def prob(self,item,cat):
    print(len(sampletrain[]))
    #print(self.totalcount())
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    strprob=self.strprob(item)
    #print(strprob)
    return docprob*catprob/strprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    #print(self.thresholds)
    if cat not in self.thresholds: return 1.0#如果不设置setthreshold中的值，此时为空，所以返回1.0
    #print(self.thresholds[cat])
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    #print('happy')
    probs={}
    max=0.0
    #print(self.categories())
    for cat in self.categories():#循环比较找到搜索词条中更优势的cat一方。
      
      probs[cat]=self.prob(item,cat)
      #print(probs[cat],cat)
      if probs[cat]>max: 
        max=probs[cat]
        #print(max)
        best=cat
        
    #print(best,'\n')

    for cat in probs:
      #print(cat)
      #print(self.getthreshold(best))
      if cat==best: continue#符合条件绕过后续内容。不符合才继续。
      #print('hhh',cat)
      #print(probs[cat],cat)
      if probs[cat]*self.getthreshold(best)>probs[best]: return default#如果满足if语句执行了return行，则跳出for循环。
      #如果good是best，这就是bad的prob值乘以getthreshold(good)值大于 good的prob值，返回unknown。
      
    #print(probs[best],best)
    return best









