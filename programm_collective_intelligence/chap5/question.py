
'''###这一段是测试代码。

a=[0,0,0,0,0,0,0,0,0,0]
question.printresult(a)
#question.matecost(a)####如果在一个py文件中写入这两个函数，python该py文件，则报错。如果分别调用。没有问题。
'''


prefs=[('Toby', ('Steve', 'Dave')),
       ('Steve', ('Karen', 'Sarah')),
       ('Karen', ('Laura','Toby')),
       ('Sarah', ('Fred', 'Jeff')),
       ('Dave', ('Toby', 'Fred')), 
       ('Jeff', ('Steve', 'Karen')), 
       ('Fred', ('Laura', 'Sarah')), 
       ('Suzie', ('Karen', 'James')), 
       ('Laura', ('Karen', 'Fred')), 
       ('James', ('Suzie', 'Dave'))]

def printresult(vec):
    '''prefs=[('Toby', ('Steve', 'Dave')),
       ('Steve', ('Karen', 'Sarah')),
       ('Karen', ('Laura','Toby')),
       ('Sarah', ('Fred', 'Jeff')),
       ('Dave', ('Toby', 'Fred')), 
       ('Jeff', ('Steve', 'Karen')), 
       ('Fred', ('Laura', 'Sarah')), 
       ('Suzie', ('Karen', 'James')), 
       ('Laura', ('Karen', 'Fred')), 
       ('James', ('Suzie', 'Dave'))]'''

    for i in range(int(len(vec)/2)):#注意要int
        for k in range(0,2):
            a = int(vec[2*i])
            
            del prefs[a]
            
        
def matecost(vec):
    cost = 0
    
    '''prefs=[('Toby', ('Steve', 'Dave')),
       ('Steve', ('Karen', 'Sarah')),
       ('Karen', ('Laura','Toby')),
       ('Sarah', ('Fred', 'Jeff')),
       ('Dave', ('Toby', 'Fred')), 
       ('Jeff', ('Steve', 'Karen')), 
       ('Fred', ('Laura', 'Sarah')), 
       ('Suzie', ('Karen', 'James')), 
       ('Laura', ('Karen', 'Fred')), 
       ('James', ('Suzie', 'Dave'))]'''

    print(prefs)#######这一行是空集。除了在函数内部声明prefs内容，有别的解决方法吗？
    for i in range(int(len(vec)/2)):
        a = int(vec[2*i])
        b = int(vec[2*i+1])
        del prefs[b]
        del prefs[a]
        