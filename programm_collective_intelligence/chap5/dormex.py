import random
import math


whatever=[('Toby', ('Steve', 'Dave')),
       ('Steve', ('Karen', 'Sarah')),
       ('Karen', ('Laura','Toby')),
       ('Sarah', ('Fred', 'Jeff')),
       ('Dave', ('Toby', 'Fred')), 
       ('Jeff', ('Steve', 'Karen')), 
       ('Fred', ('Laura', 'Sarah')), 
       ('Suzie', ('Karen', 'James')), 
       ('Laura', ('Karen', 'Fred')), 
       ('James', ('Suzie', 'Dave'))]
domain=[(0,len(whatever)-i-1) for i in range(0,len(whatever))]
#[(0,9),(0,8),(0,7),(0,6),...,(0,0)]

def printresult(vec):
    prefs = [v for v in whatever]
    
    for i in range(int(len(vec)/2)):#注意要int
        
        a = int(vec[2*i])
        #print(a)
        print(prefs[a][0])
        del prefs[a]
        b = int(vec[2*i+1])
        #print(b)
        print(prefs[b][0])
        del prefs[b]
            #print(prefs)
        print('in the same room')
        
        '''
        #哎，可惜了本来的两种写法。本来可以一起删的的。
        del prefs[a]
        print(prefs[a][0], prefs[b][0],';')
        if a>b:del prefs[b]
        else:del prefs[b-1]
        '''
        
        
def matecostnono(vec):
    cost = 0
    
    for i in range(len(vec)):
        a = int(vec[i][0])
        b = int(vec[i][1])
        prefa=prefs[a][1]
        prefb=prefs[b][1]
        if prefs[b][0] == prefa[0]:cost = cost + 0
        elif prefs[b][0] == prefa[1]: cost = cost +1
        else:cost = cost+3
            
        if prefs[a][0] == prefb[0]:cost = cost + 0
        elif prefs[a][0] == prefb[1]: cost = cost +1
        else:cost = cost+3   
    
    #print(cost)    
    return cost

def matecostold(vec):
    cost = 0
    #slots=[0,0,1,1,2,2,3,3,4,4]#哎~空宿舍的想法也用不了啦。
    for i in range(int(len(vec)/2)):
        a = int(vec[2*i])
        b = int(vec[2*i+1])
        prefa=prefs[a][1]
        prefb=prefs[b][1]
        if prefs[b][0] == prefa[0]:cost = cost + 0
        elif prefs[b][0] == prefa[1]: cost = cost +1
        else:cost = cost+3
            
        if prefs[a][0] == prefb[0]:cost = cost + 0
        elif prefs[a][0] == prefb[1]: cost = cost +1
        else:cost = cost+3   
        #del slots[0]##我真的很喜欢这个想法呀哭哭。
        #del slots[0]
    print(cost)    
    return cost
   
def matecost(vec):
    cost = 0
    prefs = [v for v in whatever]
    #print(prefs)

    for i in range(int(len(vec)/2)):#注意要int
        a = int(vec[2*i])
        #print(a)
        fir = prefs[a][0]
        prefa = prefs[a][1]
        del prefs[a]
        
        b = int(vec[2*i+1])
        #print(b)
        sec = prefs[b][0]
        prefb = prefs[b][1]
        del prefs[b]
        
        if sec == prefa[0]:cost += 0
        elif sec == prefa[1]:cost += 1
        else: cost += 3
        if fir == prefb[0]:cost += 0
        elif fir == prefb[1]:cost += 1
        else: cost += 3
    #print(cost)    
    return cost
    


a=[(5,(4,5)),(12,(1,1)),(5,(4,5)),(5,(4,5)),(12,(1,1)),(5,(4,5)),(5,(4,5)),(12,(1,1)),(5,(4,5)),(5,(4,5)),]
def kk():
    b = a
    for i in range(10):
        print(i)
        del a[i]

def zz():
    print(a)











