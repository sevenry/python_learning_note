my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

        
class decisionnode:
  def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
    self.col=col
    self.value=value
    self.results=results
    self.tb = tb
    self.fb = fb

        
def divideset(rows,column,value):
  split_function=None
   #print(isinstance(value,int))  #False isinstance是判断value是不是int类型
   #print(value)
  if isinstance(value,int) or isinstance(value,float):
    split_function=lambda row:row[column]>=value#判断column项的值是否为value
  else:
    split_function=lambda row:row[column]==value
    
    #lambda主体是一个表达式。
  #print(split_function)
  set1=[row for row in rows if split_function(row)]
  set2=[row for row in rows if not split_function(row)]
  #print(set1)#输出为“yes”项的
  #print(set2)#“no”
  return (set1,set2)
   
def uniquecounts(rows):#因为len(row)-1的值为4，即得到每一个row最后一项的值进行分类
  results={}
  for row in rows:
    #print(len(row))#5
    r=row[len(row)-1]
    #print(r)
    if r not in results:
      results[r]=0
    results[r]+=1
  #print(results,"www")
  return results

def giniimpurity(rows):#某一行数据被错误分配到另一行的概率
  total=len(rows)
  #print(total)
  counts=uniquecounts(rows)
  #print(counts)
  imp=0
  for k1 in counts:
    p1=float(counts[k1])/total
    #print(p1)
    for k2 in counts:
      if k1==k2: continue
      p2=float(counts[k2])/total
      #print(p2)
      imp+=p1*p2
  return imp

def entropy(rows):#p(i)*log(p(i)) 之和的想法。
   from math import log
   log2=lambda x:log(x)/log(2)##相当于def log2(x): a=log(x)/log(2) return a 
   results=uniquecounts(rows)
   ent=0.0
   for r in results.keys():
      p=float(results[r])/len(rows)
      #print(r,p)
      ent=ent-p*log2(p)
      #print(ent)
   return ent

def buildtree(rows,scoref=entropy):
  if len(rows)==0: return decisionnode()
  current_score=scoref(rows)

  best_gain=0.0
  best_criteria=None
  best_sets=None
  
  column_count=len(rows[0])-1
  #print(column_count)
  for col in range(0,column_count):
    column_values={}
    for row in rows:
       column_values[row[col]]=1
       #row[col]时常会重复 所以不会被重复放进字典里。
       #print(column_values)
    
    for value in column_values.keys():
      #print(value)
      (set1,set2)=divideset(rows,col,value)
      #if col==0 and value=='google':
        #print(set1,'hh')
      p=float(len(set1))/len(rows)
      gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
      if gain>best_gain and len(set1)>0 and len(set2)>0:
        best_gain=gain
        best_criteria=(col,value)
        best_sets=(set1,set2)
  
  if best_gain>0:
    #print("kkk")
    trueBranch=buildtree(best_sets[0])
    falseBranch=buildtree(best_sets[1])
    return decisionnode(col=best_criteria[0],value=best_criteria[1],
                        tb=trueBranch,fb=falseBranch)
  else:
    return decisionnode(results=uniquecounts(rows))    
    
    
####173
def printtree(tree,indent=''):
   if tree.results!=None:
      print (str(tree.results))
   else:
      print (str(tree.col)+':'+str(tree.value)+'? ')

      print (indent+'T->',)
      printtree(tree.tb,indent+'  ')
      print (indent+'F->',)
      printtree(tree.fb,indent+'  ')

def getwidth(tree):
  if tree.tb==None and tree.fb==None: return 1
  return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
  if tree.tb==None and tree.fb==None: return 0
  return max(getdepth(tree.tb),getdepth(tree.fb))+1


from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
  w=getwidth(tree)*100
  h=getdepth(tree)*100+120

  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  drawnode(draw,tree,w/2,20)
  img.save(jpeg,'JPEG')
  
def drawnode(draw,tree,x,y):
  if tree.results==None:
    w1=getwidth(tree.fb)*100
    w2=getwidth(tree.tb)*100

    left=x-(w1+w2)/2
    right=x+(w1+w2)/2

    draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

    draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
    draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
    
    drawnode(draw,tree.fb,left+w1/2,y+100)
    drawnode(draw,tree.tb,right-w2/2,y+100)
  else:
    txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
    draw.text((x-20,y),txt,(0,0,0))

    
def classify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    branch=None
    if isinstance(v,int) or isinstance(v,float):
      if v>=tree.value: branch=tree.tb
      else: branch=tree.fb
    else:
      if v==tree.value: branch=tree.tb
      else: branch=tree.fb
    return classify(observation,branch)

def prune(tree,mingain):
  if tree.tb.results==None:
    prune(tree.tb,mingain)
  if tree.fb.results==None:
    prune(tree.fb,mingain)
    
  if tree.tb.results!=None and tree.fb.results!=None:
    tb,fb=[],[]
    for v,c in tree.tb.results.items():
      tb+=[[v]]*c
    for v,c in tree.fb.results.items():
      fb+=[[v]]*c
    
    delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)

    if delta<mingain:
      tree.tb,tree.fb=None,None
      tree.results=uniquecounts(tb+fb)

def mdclassify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    if v==None:
      tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
      tcount=sum(tr.values())
      fcount=sum(fr.values())
      tw=float(tcount)/(tcount+fcount)
      fw=float(fcount)/(tcount+fcount)
      result={}
      for k,v in tr.items(): result[k]=v*tw
      for k,v in fr.items():
        if k not in result: result[k]=0
        result[k]+=v*fw
      return result
    else:
      if isinstance(v,int) or isinstance(v,float):
        if v>=tree.value: branch=tree.tb
        else: branch=tree.fb
      else:
        if v==tree.value: branch=tree.tb
        else: branch=tree.fb
      return mdclassify(observation,branch)

def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance
