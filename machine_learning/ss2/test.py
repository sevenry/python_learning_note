import kNN
from numpy import *
group,labels=kNN.createDataSet()
#print(group)
#print(labels)
#ans=kNN.classify0([0,0],group,labels,4)
#print(ans)

datingDataMat,datingLabels=kNN.file2matrix('datingTestSet.txt')
#print(datingDataMat)
#print(datingLabels[:20])


'''
import matplotlib
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()
'''

#normMat, ranges, minVals=kNN.autoNorm(datingDataMat)

#sss=kNN.datingClassTest()
#kNN.classifyPerson()

#testVector=kNN.img2vector('testDigits/0_13.txt')
#print(testVector[0,0:31])
#print(len(testVector[0]))

ans=kNN.handwritingClassTest()



