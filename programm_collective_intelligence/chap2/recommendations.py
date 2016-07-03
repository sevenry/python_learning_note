from math import sqrt


critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


def sim_distance(prefs,person1,person2):
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: 
      si[item]=1

  if len(si)==0: #判断两人是否有共同元素
    return 0
  
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])
  a = sqrt(sum_of_squares)#源代码少了开根号。
 
  return 1/(1+a)
  
def sim_pearson(prefs,p1,p2):
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: 
      si[item]=1
  
  if len(si)==0: 
    return 0

  n=len(si)
  
  sum1=sum([prefs[p1][it] for it in si])#是把每一项的得分和求出来。but how ?
  sum2=sum([prefs[p2][it] for it in si])
 
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r
  
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]
  
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    if other==person: continue
    sim=similarity(prefs,person,other)
    #print(sim)#因为sim小于零的评价值忽略，所以之后考虑的项变少。
    if sim<=0: continue#sim<=0的情况不执行后续内容，但不打破循环。
    
    for item in prefs[other]:
      if item not in prefs[person] or prefs[person][item]==0:
        print(prefs[other][item])#如果调用该函数时输入的person是Michael Phillips或者toby，则输出的print项变少。
        totals.setdefault(item,0)#字典的用法，找不到item值为0.
        totals[item] += prefs[other][item]*sim
        
        simSums.setdefault(item,0)
        simSums[item] += sim

  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  rankings.sort()
  rankings.reverse()
  return rankings
  
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      result[item][person]=prefs[person][item]
  return result