
####哭哭从雅虎密钥就开始没办法做了。伤心。

import advancedclassify
agesonly = advancedclassify.loadmatch('agesonly.csv', allnum = True)#221

'''
#matchmaker = advancedclassify.loadmatch('matchmaker.csv')
###print(agesonly[1])#如何查看？

for i in range(4):
    print(i)
row=[0,1,2,3]
print(row[0:3])

advancedclassify.plotagematches(agesonly)


avgs = advancedclassify.lineartrain(agesonly)#224

print(avgs)

dict={'a':1,'b':2,'c':3}
l=dict.setdefault(1,None)
print(l)


#####关于变量
k=0
for i in range(2):
    print(k)
    k=k+10
    for m in range(5):###如果这里是for k 的话，k的值会变成4
        print('hhh')
    
    
print(advancedclassify.dpclassify([30,25],avgs))#227
print(advancedclassify.dpclassify([25,40],avgs))
print(advancedclassify.dpclassify([48,20],avgs))


'''
advancedclassify.getlocation('1 alewife center, cambridge, ma')#230 yahoo key找不到哭哭哭哭。