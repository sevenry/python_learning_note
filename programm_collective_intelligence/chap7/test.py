###3涉及树的递归  望天  并不太懂树是怎么判断的
'''
import treepredict

#print(treepredict.divideset(treepredict.my_data,2,'yes'))#168

#print(treepredict.giniimpurity(treepredict.my_data))
#print(treepredict.entropy(treepredict.my_data))
#set1,set2=treepredict.divideset(treepredict.my_data,2,'yes')
#print(treepredict.entropy(set1))
#print(treepredict.giniimpurity(set1))#170


tree = treepredict.buildtree(treepredict.my_data)#173

#treepredict.printtree(tree)#173

#treepredict.drawtree(tree,jpeg='treeview.jpg')
#a = treepredict.classify(['digg','USA','yes',5],tree)
#print(a)

#treepredict.prune(tree,1.0)#178
#treepredict.printtree(tree)#这里也不太懂啊望天。

a=treepredict.mdclassify(['google',None,'yes',None],tree)#179
b=treepredict.mdclassify(['google','France',None,None],tree)
print(a)
print(b)

#####
import zillow
import treepredict
housedata = zillow.getpricelist()####
print(housedata)#从这一行就出错啦
housetree = treepredict.buildtree(housedata, scoref=treepredict.variance)

'''



####3
##妈蛋地址无法访问。沮丧死了。
import hotornot
ll=hotornot.getrandomratings(500)
print(len(ll))