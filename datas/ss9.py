
groupby(df['key1'],axis=0)的时候，因为key1的一组值在原来的df中是列值，是按照列来进行处理，所以axis=0##275
groupby(mapping,axis=1)的时候，因为mapping是作为columns的值进行处理，所以按行来，axis=1###280
##278
df.dtypes，然后设置轴号为1没看懂唉。
##280
people.groupby(len).sum()
len的作用是index的字符串长度。

##282
###agg是自定义函数

#284页 
（dataframe上运用函数！！！）
grouped_pct是seriesgroupby的type，=grouped['tip_pct']是选中这一项进行分析，而前面的sex和smoker相当于之前的key的标记，作为一列值传递给其中每个参数

##285页的处理方式太棒啦www
把不同的函数名作为一个list，用functions记录，同时调用其中两项数据，tip_pct,total_bill来利用functions的每个函数进行分析，而sex和smoker作为索引。##286是对不同列项进行不同的方法处理。

##287
left_on,right_index##查看pd.merge源代码

!!!!groupby(索引)###参看287页

函数运用！！函数！！！##288
transform会在datafram上对函数运用结果进行广播。

##289页 apply方法的运用
选取smoker项，对其中每项运用top函数得到排名。相当于根据索引号分为几大类，每一类进行函数运算。

##294页
range(1,11)和[10]*4分别是range和list，无法相加，应该改成list(range(1,11))+[10]*4

#296页 np.average()weights参数的意义？
&&&其实关于相关系数还是不太懂呀。是如何保证spx的相关系数为一的？是说把它作为基准比较吗？

##297页
调用regress函数的时候，第一项是'AAPL'，第二项是['SPX']是因为加的intercept=1这一项是加到spx中每个日期中的，而不是作为spx的一项存在。即应当由2214*1变成2214*2而不是2215*1

##298页
tips.pivot_table(rows=xxx)参数不是rows，应该是index

##299页
tips.pivot_table('size',index=['sex','smoker'],columns='day',aggfunc='sum')
##取出分析的是size项，利用index和columns可以进行分成几大类，如sex是两项，smoker是两项，day是四项，2*2*4种大类，每一大类调用函数如求均值等。
aggfunc='sum'的时候，是在这一大类中的所有size的值之和
如果是'len'，则是计数，这一大类中有多少个单项，与第一项'size'无关。

###300页 crosstab！！！