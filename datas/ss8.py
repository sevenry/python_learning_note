ax.plot(x,y)###x,y are not defined##246

###alpha 颜色的浓度我的天

#244 In[19]

##250
ax.legend(loc='best')###如何查看loc可以填什么内容呢。除了填错了看提示之外。
##ax.legend?? 并不能看到它的参数有哪些

##256

关于cumsum()求和的问题，默认的是0，即第一行不变，后面每行按列相加。如果参数为1，则第一列不变，后面每列按行相加。

绘图 累积值  stacked=True  259页

##259页
pd.crosstab() 我得到的结果是汇总结果而不是table##
这个问题的有趣之处在于，如果选择的两项是sex和day则是table
但是如果是size那么就得不到汇总 应该是因为com._maybe_make_list函数的问题。问题是如何针对这个问题继续查询源代码并且进行改进呢。

##如果是作图的是tips.tip和tips.day项，那么想要首先把tip项进行比如1-2,2-3这样的分类如何完成呢。
可以利用hist来作图，利用bins参数来调整区段，问题是hist是针对一维作图，所以得到的是四个表（有四天）

###262页
np.concatenate([comp1,comp2])##二者相加
comp1=array([1,1,1,1])
comp2=array([2,2,2,2])###

##字典怎么读取第一个啊。dataframe也不能读取第一个呀。好神奇。好像只有list可以读取。
series的第一项是 xx.ix[0]的读取方式。
dataframe也是利用 xx.ix[0]是读取的第一行的方式，是按照检索顺序得来。xx.ix['yyy']；yyy为第一行名称也可以
xx['ccc']读取第一列，其中ccc为第一列的名称。如果没有给出columns，则利用xx[0]的方式读取第一列
xx.ix[:,0:1]没有列名称是可以读取一二列的。有列名称则只读取了第一列。

##267页 
all_cats 是47项  是list
english_mapping是45项，过滤了重复的code。字典自动过滤重复了keys的项

unstack("xxx")如果xxx是索引名，则是unstack()的转置##290

###291
针对data1进行的数据分组，但是运用到对data2的分析上其实是错误的。
这个思路非常的有问题，把data1作为index进行检索，分成宽度相等的桶进行处理，然而所分析的数据是data2的。所以分析出来的count计数是计算符合data1分组作为检索的各项总和，而max也是根据data1的等宽标准，每一组中，各项对应的每一个data2的集合体的max。

#309页
totals=totals[totals.sum(1)>10000]###此处的sum是totals中每一行的和。
之后如果再运用totals.sum指的是列总和。
所以此处的意思是，两个人在某个地方获得的赞助超过某个值，那么可以输出他们在这一州各自得到的赞助。同时可利用totals.sum获得每个人的赞助综合。



