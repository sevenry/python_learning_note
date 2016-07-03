import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin###hhhhhhhhwwwwwwww
import sqlite3 as sqlite
import re

import nn
mynet = nn.searchnet('nn.db')
mynet.maketables()

ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}
#目前还不用：1

class crawler:

  def __init__(self,dbname):
    self.con=sqlite.connect(dbname)
  def __del__(self):
    self.con.close()

  def dbcommit(self):
    self.con.commit() 

  def getentryid(self,table,field,value,createnew=True):
    cur=self.con.execute("select rowid from %s where %s = '%s' " % (table,field,value))
    res=cur.fetchone()
    if res==None:#在table中找不到符合的value则进行插入。
      cur=self.con.execute(
      "insert into %s (%s) values ('%s')" % (table,field,value))
      return cur.lastrowid#插入记录后获取主键。虽然还是不太懂啊望天。
    else:
      return res[0] 

  def addtoindex(self,url,soup):#在crawl中调用的时候，输入的参量是pages中的一个page和soup。
    if self.isindexed(url): return#说明如果链接存在过就直接结束。
    print ('Indexing '+url)
  
    text=self.gettextonly(soup)
    words=self.separatewords(text)
    
    urlid=self.getentryid('urllist','url',url)#得到每个url的id；'url'就是字符串的url
    
    for i in range(len(words)):#从0到(len(words))不包括(len(words))
      word=words[i]
      if word in ignorewords: continue
      wordid=self.getentryid('wordlist','word',word)#'wordlist'是table名称，不需要新建。这一行保证已存储过的word不重复存储。
      self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))
      #这一行将单词放入wordlocation，它所接收的是这个链接中所有的单词。所以均对应着一个wordlocation。
       
  def gettextonly(self,soup):
    v=soup.string#获取文字
    if v==None:#为什么会为空呢
      c=soup.contents
      resulttext=''
      for t in c:
        subtext=self.gettextonly(t)
        resulttext+=subtext+'\n'
      return resulttext
    else:
      return v.strip()#删除空白符

  def separatewords(self,text):
    splitter=re.compile('\\W*')#\W是正则表达式中所有非空格；针对参数text进行去除空格
    return [s.lower() for s in splitter.split(text) if s!='']#s.lower 小写

  def isindexed(self,url):#值为True说明url存在并建立联系；值为False说明不存在。
    u=self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
    if u!=None:#如果值为None，说明在urllist中没有找到该url。所以说明url已经存在。
      v=self.con.execute('select * from wordlocation where urlid =%d' % u[0]).fetchone()
      if v!=None:#说明建立联系
        return True
    return False
  

  def addlinkref(self,urlFrom,urlTo,linkText):
    pass
    #这一段要看源代码。但是并不知道这一段作用。
   
  
  def crawl(self,pages,depth=2):#这里如果初始设定的是某一个网页，那么就只是搜这一个网页吗？depth=2的作用？p79
    for i in range(depth):
      newpages={}
      for page in pages:
        try:
          c=urllib.request.urlopen(page)
        except:
          print ("Could not open %s" % page)
          continue
        try:#书中没有try''
          soup=BeautifulSoup(c.read(),"html5lib") # 依赖于库的问题
          self.addtoindex(page,soup)#此处调用该函数中调用到gettexonly函数提取文字，接收参数是soup；下方再次使用gettexonly时参数是links中的link
          #所以二者的区分在于soup("a")和soup的区别
  
          links=soup('a')######不懂呀。
          for link in links:
            if ('href' in dict(link.attrs)):
              url=urljoin(page,link['href'])#urljoin用于合并url
              if url.find("'")!=-1: continue
              url=url.split('#')[0]  #[0]是说将原url中的第一项存为新的url？
              if url[0:4]=='http' and not self.isindexed(url):#not行说明不存在url所以需要建立新的page
                newpages[url]=1
              linkText=self.gettextonly(link)#links是soup？所以其中的子集可以作为gettexonly的参数？
              #此处调用仅是为了下一个函数服务。
              self.addlinkref(page,url,linkText)
  
          self.dbcommit()
        except:
          #print ("Could not parse page %s" % page)
          raise
      pages=newpages#把newpages中所有链接赋给pages
      #这样循环岂不是可以爬到所有链接？
      #还是说设置depth=2使得这一段仅循环两次？
      '''for xxx：
        xxxx
        xxxx 走到这一行就又要返回for行进行计数加一？如果到了边界就退出循环？
      xxx 这一行是已经退出循环了？'''

  
  # Create the database tables
  
  def createindextables(self):
    self.con.execute('create table urllist(url)')
    self.con.execute('create table wordlist(word)')
    self.con.execute('create table wordlocation(urlid,wordid,location)')
    self.con.execute('create table link(fromid integer,toid integer)')
    self.con.execute('create table linkwords(wordid,linkid)')
    self.con.execute('create index wordidx on wordlist(word)')
    self.con.execute('create index urlidx on urllist(url)')
    self.con.execute('create index wordurlidx on wordlocation(wordid)')
    self.con.execute('create index urltoidx on link(toid)')
    self.con.execute('create index urlfromidx on link(fromid)')
    self.dbcommit()
  
  def calculatepagerank(self, iterations = 20):
    self.con.execute('drop table if exists pagerank')
    self.con.execute('create table pagerank(urlid primary key, score)')
    
    self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
    self.dbcommit()
    
    for i in range(iterations):
      print("iteration % d" % (i))
      for (urlid,) in self.con.execute('select rowid from urllist'):
        pr = 0.15
        
        for (linker,) in self.con.execute('select distinct fromid from link where toid =%d' % urlid):
          linkingpr = self.con.execute('select score from pagerank where urlid = %d' % linker).fetchone()[0]#sql怎么知道pagerank是什么的呢
          
          linkingcount = self.con.execute('select count(*) from link where fromid +%d' % linker).fetchone()[0]
          pr+=0.85*(linkingpr/linkingcount)
        self.con.execute('update pagerank set score = %f where urlid =%d' % (pr, urlid))
      self.dbcommit()
	

    
    
class searcher:
  def __init__(self,dbname):
    self.con=sqlite.connect(dbname)
        
  def __del__(self):
    self.con.close()
    
  def getmatchrows(self,q):
    fieldlist='w0.urlid'#这一行也搞不明白啊。85页。
    tablelist=''
    clauselist=''
    wordids=[]
    
    words=q.split(' ')
    tablenumber=0
    
    for word in words:
      wordrow=self.con.execute(
        "SELECT rowid FROM wordlist WHERE word='%s'" % word).fetchone()#这个是在wordlist中找出搜索word的id，顺序由网页本身决定，id与搜索单词本身无关
      #print(wordrow)
      if wordrow!=None:
        wordid=wordrow[0]#依序排列，wordrow[0]是说它的顺序序列号吗？
        wordids.append(wordid)
        if tablenumber>0:
          tablelist+=','
          clauselist+=' and '
          clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1, tablenumber)#保证同一个url中出现相连的两个word，通过依次循环，保证出现所有单词
        fieldlist+=',w%d.location' % tablenumber
        tablelist+='wordlocation w%d' % tablenumber#wordlocation表中分别是(urlid,wordid,location)
        clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
        tablenumber+=1
        #print(clauselist)  #print行用于测试输出的每一项内容是否报错
        
    fullquery='SELECT %s FROM %s WHERE %s' % (fieldlist,tablelist,clauselist)#所以该行是得到了location
    #举例：从wordlocation w0中选出w0.wordid = 222的 w0.location。这里的w%d到底是什么呀。
    cur=self.con.execute(fullquery)  
    rows=[row for row in cur]
    
    #print(rows)#第一个数字是url的id，后面数字是word出现在文档中的位置，即location。那为什么会得到urlid啊。
    
    print(wordids)
    #print(rows)
    return rows, wordids
    
  
  def getscoredlist(self, rows, wordids):
    totalscores = dict([(row[0],0) for row in rows])
    #建立字典，第一项放置row[0]，调用该函数时的输入参量即getmatchrow函数输出中的rows，row[0]即是urlid，第二项放置得分。
    #得到的参量的rows是所有的rows，通过字典的方式将它们分开，即row的row[0]相同的作为一栏，并没有关心row[1]等
    
    #评价函数
    weights = [(1.0, self.nnscore(rows,wordids))]#此时调用rows仍旧是接受的参量rows，并没有根据row[0]的值进行分开，所以调用的每个评价函数需要重新建立字典。
    #weights = [(1.0, self.linktextscore(rows, wordids))]
    #weights = [(1.0, self.locationscore(rows))]
    #weights = [(1.0, self.frequencysocre(rows))]#,(1.0, self.pagerankscore(rows)),(1.0, self.locationscore(rows))]
    #weights = [(1.0, self.distancescore(rows)),(1.0, self.inboundlinkscore(rows)),(1.0, self.locationscore(rows))]
    #是依据这里的1.0作为总分实现的最高分为1分，如果是100，则转变成百分制。
     
    for (weight, scores) in weights:#此处不应该使用变量名scores，引起混乱。
      for url in totalscores:
        totalscores[url] += weight*scores[url]
        #每一个评价函数调用归一化函数，评价函数新建字典c，以[row[0],score]的形式作为归一化函数接收的参量，输出的同样是字典。
        #所以weights中每一项是(weight，[row[0],score])
        
        ##问题是totalscores中建立的字典和每一个评价函数中建立的字典是一样的呀。所以两层for循环有什么意义呢。并且吧+=改成=不影响输出结果的呀。
    return totalscores
  
  def geturlname(self, id):
    return self.con.execute("select url from urllist where rowid =%d " % id).fetchone()#根据输入的urlid，得到对应的url
    
  def query(self, q):
    rows, wordids = self.getmatchrows(q)
    scores = self.getscoredlist(rows, wordids)
    rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse = 1)
    for (score, urlid) in rankedscores[0:10]:
      #print('hhhhhhhhwwwwwwww')
      print('%f\t%s' % (score, self.geturlname(urlid)) )
      
    return wordids, [r[1] for r in rankedscores[0:10]]
  
  def normalizescores(self, scores, smallIsBetter = 0):# 所以可以根据是想要最接近还是最不接近的需求来调整参数的值是否为零即可。
    vsmall = 0.00001
    if smallIsBetter:  #if 后面接数字，如果不是零，作为true处理
      minscore = min(scores.values()) # values，items都是字典的函数。所以输入的scores变量应该是一个字典
      return dict([(u, float(minscore)/max(vsmall,k)) for (u,k) in scores.items()])#这一行如何判定最小最好的？
    else:
      maxscore = max(scores.values())
      if maxscore == 0: maxscore = vsmall
      #return dict([(u,float(c) )for (u,c) in scores.items()])
      return dict([(u, float(c)/maxscore) for (u, c) in scores.items()]) #实现归一化 是把最大值作为计数的分 所以第一名得分为1
 
 
  def frequencysocre(self, rows):
    counts = dict([(row[0], 0) for row in rows])#建立字典，将row[0]相同的分成一组。
    for row in rows: #此处是如何保证针对所有的row[0]是一个row呢，又不是in dict，而是in rows啊。row[0]相同也还是两个row啊。
      counts[row[0]]+=1#针对每一个urlid统计rows中row的个数
    return self.normalizescores(counts) #值返回给normalizescores 函数中scores一项初始值。
    #为什么只是将值返回给normalizescores函数就可以调用到这个函数中的值呢###妈蛋为了测试这个浪费了好久啊哭哭
  
  
  #位置评价方法，可改写weights一行进行调用
  def locationscore(self, rows):
    locations = dict([(row[0],1000000) for row in rows])
    for row in rows:
      loc = sum(row[1:])#p89可是这个方法统计的不是所有的row[1]的和吗。
      #如果这个单词出现的次数很多，有可能loc也会很大呀。难道不应该是选取row[0]中最小的row[1]值么。
      if loc < locations[row[0]]: locations[row[0]] = loc#其实连locations[row[0]]的值我也不理解，是后面的1000000吗？
      
    return self.normalizescores(locations, smallIsBetter = 1)
    
  def distancescore(self, rows):
    if len(rows[0])<=2:#如果只有row[0]和row[1]两项，说明仅检索了一个单词。
      return dict([(row[0],1.0) for row in rows])

    mindistance = dict([(row[0],1000000) for row in rows])
      
    for row in rows:#也就是说我还是不太懂这一行啊望天。每天都能发现新的不懂的东西出来。
      dist = sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
      if dist < mindistance[row[0]]:
        mindistance[row[0]] = dist
    return self.normalizescores(mindistance, smallIsBetter = 1)#这里如果不return直接调用不可以吗
    
  def inboundlinkscore(self, rows):
    uniqueurls = set([row[0] for row in rows])#这一行的意思？也是类似字典吗？只是还需要从中调用东西？
    inboundcount = dict ([(u, self.con.execute('select count(*) from link where toid = %d' % u).fetchone()[0])for u in uniqueurls])
    #link没有定义啊，sql是怎么知道它是啥意思的？包括前面的rowid？
    
    return self.normalizescores(inboundcount)#返回给normalizescores的是一个字典
    
  def pagerankscore(self, rows):#该函数仅仅是把pagerank的分数取出
    pageranks = dict([(row[0], self.con.execute \
      ('select score from pagerank where urlid =%d' % row[0]).fetchone()[0]) for row in rows])
    #return self.normalizescores(pageranks)或者利用该行取代以下三行即可
    maxrank = max(pageranks.values())
    normalizescores = dict([(u, float(k)/maxrank) for (u,k) in pageranks.items()])#这个已经做了归一化处理，不需要再经过normalizescores函数
    return normalizescores
    
  def linktextscore(self, rows, wordids):
    linkscores = dict ([(row[0],0) for row in rows])
    for wordid in wordids:
      cur = self.con.execute('select link.fromid,link.toid from linkwords, link where\
        wordid = %d and linkwords.linkid = link.rowid' % wordid)#所以rowid是序数？
      for (fromid, toid) in cur:
        if toid in linkscores:#为什么不是fromid，link表中是(fromid integer,toid integer)
          pr = self.con.execute('select score from pagerank where urlid =%d' % fromid).fetchone()[0]#为什么fromid是urlid啊。
          linkscores[toid] += pr
    return self.normalizescores(linkscores)
    #maxscore = max (linkscores.values())
    #normalizescores = dict([(u, float(k)/maxscore) for (u,k) in linkscores.items()]) 
    #return normalizescores
    
  def nnscore(self, rows ,wordids):
    urlids = [urlid for urlid in set([row[0] for row in rows])]
    #print(urlids)
    #print(len(urlids))
    #for i in range(3):
        #print(rows[0][i],i)
    mn=min(len(urlids),5)
    #for i in range(mn):
    mynet.trainquery(wordids,urlids,urlids[0])#这个函数写的不好，最后一个参数项应当接受比如频率最高的url。
    nnres = mynet.getresult(wordids, urlids)
    scores = dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
    return self.normalizescores(scores)
    
