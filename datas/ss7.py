lefth=dff({'key1':['ohio','ohio','ohio','nevada','nevada'],'key2':[2000,2001,2002,2001,2002],'data':np.arange(5)})

righthhh=dff({'key1':['ohio','ohio','ohio','ohio','nevada','nevada'],'key2':[2001,2000,2000,2000,2003,2004],'data':np.arange(12).reshape((6,2))})


righth=dff(np.arange(12).reshape((6,2)),index=[['nevada','nevada','ohio','ohio','ohio','ohio'],[2005,2006,2000,2000,2003,2004]],columns=['event1','event2'])

pd.merge(lefth,righth,left_on=['key1','key2'],right_index=True)

pd.merge(lefth,righth,left_on=['key1'],right_index=True)###这样写有问题的原因是，righth是利用了索引的形式，left_on必须是两项，要符合和righth的levels一致。

left1.join(right1,on='key')###right1引用了索引，索引需要调用on作为参数，建立联系。

combine_first()#209页。感觉不太清楚呢。

pivot##总是不对呢。212页。ldata.csv在ch07中#######

col行算randn(1000,4)这里，随机数结果都一样为啥。。。#222

permutations##223

set.unions###

get_dummies###225重看呀~~~
