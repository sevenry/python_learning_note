import sss
'''
#这一段是说搜索得到db文档；问题是加上class searcher后无法进行搜索。
#imp.reload(sss)  #妹的imp也说没有我也是醉了啊
crawler=sss.crawler('searcherindex.db')
crawler.createindextables()
page=['https://en.wikipedia.org/wiki/Jon_Snow']
crawler.crawl(page)
'''

e=sss.searcher('searcherindex.db')#在db文档中检索是否已经是不需要关联互联网，后续的评价仅针对爬下来的网页进？



#e.getmatchrows('robert rose king jon happy ') 
#e.getmatchrows('winter jon snow rose robert') #p86文中会出现位置结果需要多一行print内容，而为了之后query函数调用该函数不输出位置故隐去print
#搜索两个词，均存在的情况下，rows是三个一组的列表，wordid是有两个
#rose happy 可以搜得到 sad好像不可以。

e.query('king rose snow jon hurt')
e.query('kingdom kill snow')
e.query('north stanley win')
e.query('snow rose')
e.query('god south snow study')
#如果是调用nn.py文件的话，并不知道如何像书上105页说的一样传递结果呀。所以我在nnscore函数中加了两句，但是感觉不太对呀。
#87页测试函数  

#e.frequencysocre(self, rows)



##为啥不能直接写函数进行调用呀。

'''
s=sss.aaa()
print("hhh")

def aaa(self,k):
    
    print("333")
    return bbb
    
def bbb(self):
  print("kkk")




crawler=sss.crawler('searcherindex.db')
crawler.calculatepagerank()



Cu=crawler.con.execute('select * from pagerank order by score desc')
for i in range(3):
  print(Cu())###这一行无法测试。书上94页。
    
e.geturlname(4)
'''