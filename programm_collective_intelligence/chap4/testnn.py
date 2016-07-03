import nn
mynet = nn.searchnet('nn.db')

#mynet.maketables()
#这段代码调用的时候总会提醒nn.db已经存在，需要删除该行，这一行是调用该函数执行创建table的。

#wjon, sad, wRose, wsnow,god,nut,kate,pig= 105,102,103,106,34,23,34,31
#uSnowRose,uHappy,uRobert,kimi,sarah= 201,202,203,88,99
robert ,rose ,king ,jon ,happy=1301,1287,1819,2,9875
u1,u2,u3,u4,u5=9,43,59,76,100
#mynet.generatehiddennode([wSnow, wRose],[uSnowRose,uHappy,uRobert])

'''
for c in mynet.con.execute('select * from wordhidden'):
    print(c)

for c in mynet.con.execute('select * from hiddenurl'):
    print(c)
#这里打印的c是wordhidden和hiddenurl的内容  
'''

#mynet.getallhiddenids([wSnow, wRose], [uSnowRose,uHappy,uRobert])

#这一个函数负责根据相应的wordids的组合生成hiddenid。每输入一次新的wordids的组合，就会有一个新的值。
#如果一个word出现在好几个wordids中，那么这个word就跟不同的hiddenid可以在setstrength中均生成strength。而不需要使用默认的-0.2和0。
#mynet.generatehiddennode([nut,kate,god],[uSnowRose,uRobert])
#mynet.generatehiddennode([god, wRose,wjon],[uHappy,uSnowRose])
#mynet.generatehiddennode([wsnow, ad],[uSnowRose,uRobert])
#mynet.generatehiddennode([god, wsnow],[uSnowRose,uHappy,uRobert])
#mynet.generatehiddennode([pig,wsnow],[uSnowRose,uRobert])
#mynet.generatehiddennode([pig,wsnow],[kimi,sarah])

#mynet.setupnetwork([god, wRose,wjon],[uHappy,uSnowRose])
#mynet.setupnetwork([pig,wsnow],[uSnowRose,uRobert])
#mynet.setupnetwork([pig,wsnow],[kimi,sarah])

#mynet.feedforward

#mynet.updatedatabase

#mynet.generatehiddennode([nut,sad],[kimi,sarah])
#mynet.setupnetwork([nut,sad],[kimi,sarah])
#mynet.feedforward()

#mynet.getresult([nut,sad],[kimi,sarah])#缺少保存项，所以如果为了反复推演，应当不断调用trainquery函数。

#wjon, sad, wRose, wsnow,god,nut,kate,pig= 105,102,103,106,34,23,34,31
#allurls=[uRobert,kimi,sarah]
for i in range(3):
    mynet.trainquery([rose ,king,jon ],[u1,u2,u3],u1)
    '''mynet.trainquery([nut,sad],allurls,sarah)
    mynet.trainquery([wjon,wRose],allurls,sarah)
    mynet.trainquery([nut,wRose],allurls,sarah)
    mynet.trainquery([nut,god],allurls,sarah)
    mynet.trainquery([wsnow,god],allurls,sarah)
    mynet.trainquery([kate,pig],allurls,sarah)
    
mynet.getresult([nut,sad],allurls)
mynet.getresult([wjon,wRose],allurls)
mynet.getresult([nut,wRose],allurls)
mynet.getresult([nut,god],allurls)
mynet.getresult([wsnow,god],allurls)
mynet.getresult([kate,pig],allurls)
mynet.getresult([nut],allurls)'''
