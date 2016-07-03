import recommendations 
from math import sqrt
#import pydilicious
#import maybe #修改过的python3的版本且删除了废话的。
import noway  #感觉调用get_popular函数所用到的部分都在这了。
##第二章后面的内容还是可以继续做的。www

'''
print(critics['Lisa Rose']['Lady in the Water'])
critics['Toby']['Snakes on a Plane'] = 4.5
print(critics['Toby'])#输出的顺序是随机的唉。

a = 1/(1+sqrt(pow(4.5-4,2)+pow(1-2,2)))
print(a)


b = recommendations.sim_distance(recommendations.critics, 'Lisa Rose', 'Gene Seymour')
print(b)
c = recommendations.sim_pearson(recommendations.critics, 'Lisa Rose', 'Gene Seymour')
print(c)


k = recommendations.topMatches(recommendations.critics, 'Toby', n=6)
print(k)

g = recommendations.getRecommendations(recommendations.critics, 'Toby')
print(g)


movies = recommendations.transformPrefs(recommendations.critics)
mm = recommendations.topMatches(movies, 'Superman Returns')
#print(mm)
ww =  recommendations.getRecommendations(movies, 'Lady in the Water')
print(ww)'''

a = noway.get_popular(tag = 'programming')
print(a)#42页。我真的是无能为力啦。 