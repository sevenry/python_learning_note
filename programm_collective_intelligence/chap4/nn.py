from math import tanh
from sqlite3 import dbapi2 as sqlite

def dtanh(y):
    return 1.0 - y * y

class searchnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
        
    def __del__(self):
        self.con.close()
        
    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid, toid, strength)')
        self.con.execute('create table hiddenurl(fromid, toid, strength)')
        self.con.commit()#sql执行了DML语句后使用该句进行提交。
        
    def getstrength(self, fromid, toid, layer):
        if layer == 0:
            table = 'wordhidden'
        else:
            table = 'hiddenurl'
        res = self.con.execute('select strength from %s where fromid = %d and toid = %d' %\
            (table, fromid, toid)).fetchone()#这一行是针对两个表格都建立了内容。根据后文利用layer的数值分别调用，输入的fromid和toid不同，表格内容不同
        if res == None:
            if layer == 0:
                return -0.2
            if layer == 1:
                return 0
        #print (res[0])#这两句print都没有输出内容为什么啊。
        return res[0]#所以输出的是列表还是矩阵？
        
    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = 'wordhidden'
        else:
            table = 'hiddenurl'
        res = self.con.execute('select rowid from %s where fromid = %d and toid = %d' %\
            (table, fromid, toid)).fetchone()
            #在测试行将单词已经转化成数字了。所以测试的时候是wordids和urlids是单词，但是这里接收的fromid和toid都是数字
        #print('lalala')
        #print(res) #为什么我已经再次调用同一个generatehiddennode函数的时候，还是返回none？不应该已经存在表格中了么？？？？
        if res == None:
            self.con.execute('insert into %s (fromid, toid, strength) values (%d, %d, %f)' %\
                (table, fromid, toid, strength))
                #99页输出的三个数字的意思在这个函数里分别是 fromid，toid，strength
            #print('ccc')
            #print(fromid, toid, strength)
        else:
            rowid = res[0]#通过这一行保证，后续重新调用的时候，即使fromid和toid都存在，也可以替换rowid为新的得到的strength。
            
            #print('hhh')
            #print(rowid)
            self.con.execute('update %s set strength = %f where rowid = %d' %\
                (table, strength, rowid))
        #调用这个函数如果print结果，是none？是因为无返回值默认返回none？
     
    def generatehiddennode(self, wordids, urls):#urls应该用urlids更便于理解。
        #if len(wordids) > 3:#所以只能检索两个单词之间的关系？
        #    return None
        createkey = '_'.join(sorted([str(wi) for wi in wordids]))#str()将数值转化成字符串
        res = self.con.execute("select rowid from hiddennode where create_key = '%s' " % createkey).fetchone()
        #hiddennode表中即(create_key)项。
        #print(res)#如果换一组词进行搜索时这一行函数会打印none，下面的print就会是2.
        ### 如果我在py文件中写两次同一个函数，第二次是print是1，如果我是py中一个函数，powershell中调用两次，那么print都是none。好奇怪！
        if res == None:
            cur = self.con.execute("insert into hiddennode (create_key) values ('%s')" % createkey)#hiddennode 表中是节点位置
            hiddenid = cur.lastrowid#插入记录后获取主键
            #print(hiddenid)
            for wordid in wordids:#对wordids中的每一项创建链接
                self.setstrength(wordid, hiddenid, 0, 1.0/len(wordids))#setstrength中的fromid即这里的wordid，toid即hiddenid，0是单词到隐藏层
                #即该函数针对给定的wordids链接输出权重（即连接强度）
                #这一行也说明了strength本身就与hiddenid无关。
                #print(self.setstrength(wordid,hiddenid,0,1.0/len(wordids)))该行和上一行颠倒顺序输出不同。
                
            for urlid in urls:
                self.setstrength(hiddenid, urlid, 1, 0.1)#这一行则针对给定的urlids链接输出隐藏层的节点号，urlid和权重
            #self.con.commit()
     
    def getallhiddenids(self, wordids, urlids):
        ll={}
        
        for wordid in wordids:
            cur = self.con.execute(
            'select toid from wordhidden where fromid = %d' % wordid)#wordhidden表中(fromid,toid,strength)，其中fromid即wordid
            #找到的是表中对应隐藏层的id
            
            for row in cur :
                ll[row[0]] = 1
            
        for urlid in urlids:
            cur = self.con.execute(
            'select fromid from hiddenurl where toid = %d' % urlid)#hiddenurl表中(fromid,toid,strength),其中toid为urlid
            #找到的是表中隐藏层到url的id
            #print(cur)#这个输出非常奇怪。hhh完全看不懂。
            for row in cur:
                ll[row[0]] = 1
                
        #这里得到的值为什么不都是1？        
        #这两段循环到最后会留下所有内容。但是根据不同的wordids和urlids的组合，每一个word和url出现过的hiddenid都被收集。以确保后续进行得到连接强度的时候，
        #所有的wordid和urlid都与‘与它们分别有关的hiddenid’发生关联。
                
        #print(ll.values())#是urlid行得到。
        #print(ll.items())#结果是dict_items([(1,1)])第一个1是keys，第二个1是由urlid行得到。可是输入的不都是row[0]吗，为啥不都是1呢我还是想问。
        #真是被自己蠢哭了，这里都生成了字典了字典了字典了我还在这折腾哭瞎了。不过是怎么生成的？因为ll[row[0]]=1吗
        #print (ll.keys())#结果是所有之前调用过的generatehiddennode的合集。比如建了10次新的wordids并调用了那个函数，则出现1-10.
        return ll.keys()
          
    def setupnetwork(self, wordids, urlids):
        self.wordids = wordids
        self.hiddenids = self.getallhiddenids(wordids, urlids)#此处的hiddenids是利用上一个函数计算得到，而不是节点位置得到。
      
        print(self.hiddenids)
        self.urlids = urlids
        
        self.ai = [1.0] * len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)
        
        self.wi = [[self.getstrength(wordid, hiddenid, 0)#为什么此处调用这个函数不输出getstrength内部的print语句的内容啊。
        #即在wordhidden表中找到hiddenid为1至之前输入的wordids的次数，fromid=wordid的strength；strength则是调用setstrength函数时输入的。
        #而在setstrength函数中，strength的设定是由generateallhiddenids决定的，本身值就只与wordid有关。
                    for hiddenid in self.hiddenids]
                    for wordid in self.wordids]
        self.wo = [[self.getstrength(hiddenid, urlid, 1)
                    for urlid in self.urlids]
                    for hiddenid in self.hiddenids]
        
        #print(self.wi)#比如之前wordids调用过setupnetwork函数10次，该次检索的wordids=3,那么会出现三组结果，每组十个数。如果有匹配过的hiddenid，
        #输出的则是setstrength中的值，否则为0.2.所谓匹配过的意思是，该word和在之前的generatehiddennode函数中出现过，所以在table中有值可选。
        
        #print(self.wo)#因为wo和wi的for语句不同，所以这边出现的是10组，每组的个数是根据urlids的个数而定。而如果每次新建hiddenid的时候只是更换了wordids，
        #而没有变动urlids，那么输入新的urlids，得出的值也往往都是0，因为hiddenid是否新建是根据wordids决定。
        
    def feedforward(self):
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0
            
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]#来自输入层的结果乘以连接强度 p101
            self.ah[j] = tanh(sum)
            
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]#j是hiddenid的节点号，k是urlid的节点号。
            self.ao[k] = tanh(sum)
        
        #print((self.ao[:]))#该行保证输出  print行必须在return行之前才能输出
        return (self.ao[:])
        
    def feedforward1(self):
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0
            
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]#来自输入层的结果乘以连接强度 p101
            self.ah[j] = tanh(sum)
            
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]#j是hiddenid的节点号，k是urlid的节点号。
            self.ao[k] = tanh(sum)
        
        #print((self.ao[:]))#该行保证输出  print行必须在return行之前才能输出
        return (self.ao[:])
       
    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward1()#书上是如何做到，调用trainquery函数不输出结果，但是在getresult中就输出结果呢。
        #我唯一想到的方法是重建函数。
        
    def backPropagate(self, targets, N = 0.5):
        output_deltas = [0.0] * len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k]) * error    
        hidden_deltas = [0.0] * len(self.hiddenids)
        
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error = error + output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j]) * error
            
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change
                #print(self.wo[j][k])
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change =hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change
                print(self.wi[i][j])
        return #这一行的意思是？将wi和wo都返回还是？但是在trainquery中如果print这个函数则为空啊。
        #利用这个函数调整了所有的wi和wo的值。
    
    '''def updatenew(self):
        #maybe = dict([(self.wordids[0],0) for wordid in self.wordids])
        #dicth = dict([(self.hiddenids[0],0) for hiddenid in self.hiddenids])
        for wordid in self.wordids:
            for hiddenid in self.hiddenids:
                self.setstrength(wordid, hiddenid, 0, self.wi[wordid][hiddenid])
                
        for urlid in self.urlids:
            for hiddenid in self.hiddenids:
                self.setstrength(hiddenid, urlid, 1, self.wo[urlid][hiddenid])
        self.con.commit()        #这样的编写方式无法完成self.wi[i][j],下面的则通不过hiddenids[j]'''
    
    def updatedatabase(self):
    #这个非常奇怪，刚开始没有隐去这段函数，只要调用的时候隐去就没问题，现在就必须要隐去否则总是报错。
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                #self.con.execute('insert into %s (fromid, toid, strength) values (%d, %d, %f)' %\
                #('wordhidden', self.wordids[i], list(self.hiddenids)[j], self.wi[i][j]))
                #print("kkk")如果改成print行输出没有问题。说明是以下两句语法问题。加上return 也不行。望天。
                #self.setstrength(self.wordids[i],j, 0, self.wi[i][j])
                #这样编译是可以的，如果i，j换成self.hiddenids[i]则不行。
                self.setstrength(self.wordids[i], list(self.hiddenids)[j], 0, self.wi[i][j])
                #print(self.wordids)
                #print(self.hiddenids)因为它是字典。因为它是字典。因为它是字典。
        for j in range(len(self.hiddenids)):
           for k in range(len(self.urlids)):
        #        self.con.execute('insert into %s (fromid, toid, strength) values (%d, %d, %f)' %\
        #        ('hiddenurl', self.hiddenids[j], self.urlids[k], self.wi[j][k])
                #print("www")
                #self.setstrength(j, self.urlids[k], 1, self.wo[j][k])
                self.setstrength(list(self.hiddenids)[j], self.urlids[k], 1, self.wo[j][k])
        self.con.commit()
        
        
    
    def trainquery(self, wordids, urlids, selectedurl):
        self.generatehiddennode(wordids, urlids)#重复调用这个函数的时候因为取值不为空，所以不会继续调用setstrength函数，所以strength不会恢复原始值，
        #而保留updabase的值。
        
        self.setupnetwork(wordids, urlids)
        self.feedforward()
        targets = [0.0] * len(urlids)
        #print(urlids)#符合所有检索要求的urlid的输出
        #print(targets)#符合要求的url的个数。
        targets[urlids. index(selectedurl)] = 1.0
        #print(targets)
        self.backPropagate(targets)
        #print(self.backPropagate(targets))#为空啊。
       
        self.updatedatabase()
        ####self.updatenew()