def kk(a,b):
    def mm(c):
        return  c+1+3
    return mm
    
    

def www(fff):
    i = 0
    while i < 1:
     
        a=fff(i)#在后面调用函数的时候如何知道i是传给kk中的mm的c的位置呢。
        
        i=i+1
    return a 
    

a=11
b=3
fff=kk(a,b)
print(www(fff))
    