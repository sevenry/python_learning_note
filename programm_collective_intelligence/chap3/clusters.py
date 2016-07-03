from PIL import Image,ImageDraw #可能会报错呢。
from math import sqrt
import random

def readfile(filename):
  lines=[line for line in open(filename)]###oh no
  
  colnames=lines[0].strip().split('\t')[1:]
  #print(colnames[1])
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    rownames.append(p[0])#每行的第一列是行名。
    
    data.append([float(x) for x in p[1:]])#剩下的该行对应的数据。
  #print(rownames[1])
  #print(data[1][2])
  return rownames,colnames,data
  
def pearson(v1,v2):
  sum1=sum(v1)
  sum2=sum(v2)
  
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])	
  
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-num/den#36页说皮尔逊评价值是-1到1之间，那么这个值也应该是-1到1之间呀。
  
class bicluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.id=id
    self.distance=distance

def hcluster(rows,distance=pearson):
  distances = {}
  currentclustid = -1
 
  clust=[bicluster(rows[i],id=i) for i in range(len(rows))]#这里调用了bicluster，并确保id为i。
  #print(clust[0])#这个是啥，看不懂哎。
  #print(clust[3].vec)#clust[i].vec即rows[i]
  #print(clust[1].id)
  #print(len(clust))#99
  while len(clust)>1:
    lowestpair=(0,1)
    closest=distance(clust[0].vec,clust[1].vec)
    #print(clust[0])#为什么每次输出结果不一样啊。
    #print(closest)#输出的个数为98个

    for i in range(len(clust)):
      for j in range(i+1,len(clust)):
        if (clust[i].id,clust[j].id) not in distances: 
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
          
        d=distances[(clust[i].id,clust[j].id)]

        if d<closest:
          closest=d
          lowestpair=(i,j)#暂时存储i,j的数值。
    #整个for循环是在所有的clust中找到最近的两个队列。
    
    #lowestpair[0] = i（之前找到的最近的两个类的id之一）
    mergevec=[
    (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 
    for i in range(len(clust[0].vec))]
    #print(len(clust[0].vec))#706

    newcluster = bicluster(mergevec,left=clust[lowestpair[0]],
                           right=clust[lowestpair[1]],
                           distance=closest,id=currentclustid)
    #print(clust[lowestpair[1]])#准确说我不太懂这一行…… 输出的内容也不太看得懂
    currentclustid-=1
    #print(currentclustid)
    del clust[lowestpair[1]]#仅仅是在原来的大的clust中删除了这两个队列，而放入了新的队列作为left和right。通过最开始的class的部分保存了所有的id，left等信息。
    del clust[lowestpair[0]]
    clust.append(newcluster)
  #print(len(clust))#此时只有1 因为不断合并成为一个聚类。
  #print(clust[0])#此时输出的是新的聚类的值了。为什么这个输出值不同啊。
  #print(clust[1])#此时这样子已经不存在了呀。
  return clust[0]
  

def printclust(clust,labels=None,n=0):
  for i in range(n):#完全不懂这一行。而且我也没办法查看。显示页面不够到最开始的呀。如果调整上一个函数中while > 96等，又不能成为一棵树。
    print (' ',)
  if clust.id < 0:
    print ('-')
  else:
    if labels==None: 
      print (clust.id)
    else: 
      #print (clust.id)#id依旧存在。
      print (labels[clust.id])

  if clust.left!=None: 
    printclust(clust.left, labels=labels, n = n+1)
  if clust.right!=None: 
    printclust(clust.right, labels=labels, n = n+1)
    
def getheight(clust):
  if clust.left==None and clust.right==None: 
    return 1

  return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
  if clust.left==None and clust.right==None: 
    return 0

  return max(getdepth(clust.left),getdepth(clust.right)) + clust.distance

def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
  h=getheight(clust)*20
  w=1200
  depth=getdepth(clust)

  scaling=float(w-150)/depth

  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  draw.line((0,h/2,10,h/2),fill=(255,0,0))    

  drawnode(draw,clust,10,(h/2),scaling,labels)
  img.save(jpeg,'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):#这个函数因为采用的是递归，所以第一个先化的是竖线而不是横线。
  if clust.id<0:
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    
    ll=clust.distance*scaling
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    
    
    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    

    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        

    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:   
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))
    
'''
def newdraw(draw,clust,10,(h/2),scaling,labels):#如果采用先画横线再竖线的情况会出问题。当一个节点左分支为枝，右分支为叶，就会出错。
  if clust.id < 0 :
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    
    ll=clust.distance*scaling
    draw.line((x,y,x+ll,y),fill=(255,0,0))   
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))   
    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:   #以及else根本没办法写呀。
    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))
    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))
  
'''
    
def rotatematrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata
    
def kcluster(rows,distance=pearson,k=4):
  #print(len(rows))#99
  #print(len(rows[0]))#706
  ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) 
  for i in range(len(rows[0]))]#范围指的是，rows中每一个row中（用 for row in rows 实现）每一个位置（range实现）
  #的最小值和最大值，所以len的是rows[i],得到每一个row的元素个数，而不是rows。
  '''print (ranges[3])
  print (ranges[6][0])#[i][0]往往都是0，是由于对应着最小值，
  print (ranges[6][1])#对应着每一个row中第[i]位置上的最大值。'''
  
  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
  for i in range(len(rows[0]))] for j in range(k)]#创造k个中心点 虽然不懂为啥是这样创建。random.random()不懂哎。
  #print(len(clusters[3]))#得到的clusters有k项，每一项有706个元素。
  lastmatches=None
  for t in range(100):#100是保证次数足够多能够得到匹配？
    print ('Iteration %d' % t)
    bestmatches=[[] for i in range(k)]
    #print (bestmatches)#输出均为[[],[],[],[],[],[]],内部[]的个数为k。
    for j in range(len(rows)):
      row=rows[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],row)
        if d < distance(clusters[bestmatch],row): 
          bestmatch = i
      bestmatches[bestmatch].append(j)#对每一个row来说，寻找到最接近的中心点k，将row的序列号j放入对应的中心点k的队列中。

    if bestmatches==lastmatches: break#直到后续循环不发生变化打破。
    lastmatches=bestmatches
    #print(len(bestmatches[1]))#得到的是与第i个中心点距离最近的row的个数。
    for i in range(k):
      avgs=[0.0]*len(rows[0])
      #print(len(avgs))#同样是706，print(avgs)的结果是0.0
      #print(avgs)
      if len(bestmatches[i]) > 0:
        for rowid in bestmatches[i]:
          #print((len(rows[rowid])))#此处得到的也是rows中每一个row的元素个数
          for m in range(len(rows[rowid])):
            avgs[m] += rows[rowid][m]#把同一个聚类中对应位置的项全部加在一起
        for j in range(len(avgs)):
          avgs[j] /= len(bestmatches[i])#除以同一个聚类中row的个数得到平均值。
        clusters[i] =avgs
      
  return bestmatches#

def tanimoto(v1,v2):
  c1,c2,shr=0,0,0
  
  for i in range(len(v1)):
    if v1[i]!=0: c1+=1 # in v1
    if v2[i]!=0: c2+=1 # in v2
    if v1[i]!=0 and v2[i]!=0: shr+=1 # in both
  
  return 1.0-(float(shr)/(c1+c2-shr))

def scaledown(data,distance=pearson,rate=0.01):
  n=len(data)
  #print(n)#99,data即99组706个元素的row的集合。

  realdist=[[distance(data[i],data[j]) for j in range(n)] 
             for i in range(0,n)]
  
  outersum = 0.0

  loc=[[random.random(),random.random()] for i in range(n)]#生成了二维坐标系。
  #print(len(loc[0]))#2;len(loc):99
  fakedist = [[0.0 for j in range(n)] for i in range(n)]
  #print(len(fakedist[0]))#99;len(fakedist):99
  
  lasterror=None
  for m in range(0,1000):
    for i in range(n):
      for j in range(n):
        fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) 
                                 for x in range(len(loc[i]))]))#x的取值是0或者1
  
    grad=[[0.0,0.0] for i in range(n)]
    
    totalerror=0
    for k in range(n):
      for j in range(n):
        if j==k: continue
        errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]#书上这一行的缩进应该不对。73页。
        
        grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
        grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

        totalerror+=abs(errorterm)#abs绝对值函数
    #print (totalerror)

    if lasterror and lasterror < totalerror: 
      break
    lasterror = totalerror
    
    for k in range(n):
      loc[k][0]-=rate*grad[k][0]
      loc[k][1]-=rate*grad[k][1]

  return loc

def draw2d(data,labels,jpeg='mds2d.jpg'):
  img=Image.new('RGB',(2000,2000),(255,255,255))
  draw=ImageDraw.Draw(img)
  for i in range(len(data)):
    x=(data[i][0]+0.5)*1000
    y=(data[i][1]+0.5)*1000
    draw.text((x,y),labels[i],(0,0,0))
  img.save(jpeg,'JPEG')  

