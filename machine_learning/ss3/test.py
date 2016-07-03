import trees
mydat,labels=trees.createDataSet()
#mydat[0][-1]='maybe'
#print(mydat)
'''
cc=trees.calcShannonEnt(mydat)
print(cc)

aa=trees.splitDataSet(mydat,0,1)
print(aa)
bb=trees.splitDataSet(mydat,1,0)
print(bb)

kk=trees.chooseBestFeatureToSplit(mydat)
print(kk)
'''

#mytree=trees.createTree(mydat,labels)
#print(mytree)

import treePlotter
#treePlotter.createPlot()
#dd=treePlotter.retrieveTree(1)
#print(dd)
myTree=treePlotter.retrieveTree(0)
#print(myTree)
#a=treePlotter.getNumLeafs(myTree)
#b=treePlotter.getTreeDepth(myTree)
#print(a,b)

#treePlotter.createPlot(myTree)####

aa=trees.classify(myTree,labels,[1,1])
print(aa)