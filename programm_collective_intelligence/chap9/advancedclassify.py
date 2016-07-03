class matchrow:
  def __init__(self,row,allnum=False):
    if allnum:
      self.data=[float(row[i]) for i in range(len(row)-1)]#for i in range(k),是从0对k—1，故不输出最后一项
    else:
      self.data=row[0:len(row)-1]#从0位开始（即第一项）输出len(row)-1项，故不输出最后一项
    #print(self.data)
    self.match=int(row[len(row)-1])#在这里给match赋值，即获得数据中最后一项的值。

def loadmatch(f,allnum=False):
  rows=[]
  for line in open(f):
    rows.append(matchrow(line.split(','),allnum))#如何查看每一行的matchrow的data部分呢。
  return rows

from pylab import *
def plotagematches(rows):
  xdm,ydm=[r.data[0] for r in rows if r.match==1],\
          [r.data[1] for r in rows if r.match==1]
  xdn,ydn=[r.data[0] for r in rows if r.match==0],\
          [r.data[1] for r in rows if r.match==0] 
  
  plot(xdm,ydm,'go')
  plot(xdn,ydn,'ro')#绿色部分
  
  show()

def lineartrain(rows):
  averages={}
  counts={}
  #k=0#此处所有变量均应用k而不能是i，因为后面的循环中变量名是i，会认为i一直为1
  #print(len(rows))
  for row in rows:
    cl=row.match
    #print(cl)
    #if k ==0:print(row.data[0],row.match)
    #print(k)
    #k+=1
    #k=4
    ###dict.setdefault(key, default)#在字典中查找key，如果没有符合的就返回default。
    ###dict={key1:v1,key2:v2}# dict.setdefault(key1,a) 返回v1
    
    m=averages.setdefault(cl,[0.0]*(len(row.data)))
    #if k==0:print(m)
    
    counts.setdefault(cl,0)
    #print(len(row.data))
    for i in range(len(row.data)):
      #print(row.data[i],i,'hh')
      #print(averages[cl][i],'bf')

      averages[cl][i]+=float(row.data[i])
      #print(averages[cl][i],cl)
      
    counts[cl]+=1
  
  for cl,avg in averages.items():
    for i in range(len(avg)):
      #print(len(avg))
      avg[i]/=counts[cl]
  
  return averages

def dotproduct(v1,v2):
  return sum([v1[i]*v2[i] for i in range(len(v1))])

def dpclassify(point,avgs):
  b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
  y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b
  if y>0: return 0
  else: return 1


def yesno(v):
  if v=='yes': return 1
  elif v=='no': return -1
  else: return 0

def matchcount(interest1,interest2):
  l1=interest1.split(':')
  l2=interest2.split(':')
  x=0
  for v in l1:
    if v in l2: x+=1
  return x

def milesdistance(a1,a2):
  lat1,long1=getlocation(a1)
  lat2,long2=getlocation(a2)
  latdif=69.1*(lat2-lat1)
  longdif=53.0*(long2-long1)
  return (latdif**2+longdif**2)**.5

yahookey="YOUR API KEY"###where can i ???
from xml.dom.minidom import parseString
import urllib

loc_cache={}
def getlocation(address):
  if address in loc_cache: return loc_cache[address]
  data=urllib.request.urlopen('http://api.local.yahoo.com/MapsService/V1/'+\
               'geocode?appid=%s&location=%s' %
               (yahookey,urllib.parse.quote_plus(address))).read()
  doc=parseString(data)
  lat=doc.getElementsByTagName('Latitude')[0].firstChild.nodeValue
  long=doc.getElementsByTagName('Longitude')[0].firstChild.nodeValue  
  loc_cache[address]=(float(lat),float(long))
  return loc_cache[address]























