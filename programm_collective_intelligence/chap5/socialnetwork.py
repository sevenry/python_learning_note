import math
from PIL import Image,ImageDraw

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'), 
       ('Mike', 'Joe'), 
       ('Miranda', 'Mike'), 
       ('Violet', 'Augustus'), 
       ('Miranda', 'Willy'), 
       ('Charlie', 'Mike'), 
       ('Veruca', 'Joe'), 
       ('Miranda', 'Augustus'), 
       ('Willy', 'Augustus'), 
       ('Joe', 'Charlie'), 
       ('Veruca', 'Augustus'), 
       ('Miranda', 'Joe')]

def crosscount(v):
  loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
  #print(loc)
  total=0
  
  for i in range(len(links)):
    for j in range(i+1,len(links)):

      (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
      (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
      
      den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)#本质是两个直线的k值相减

      if den==0: continue

      ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den#本质是求得交点坐标x，(x-x1)/(x2-x1) 的值介于0到1之间认为交点在线段上。
      ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
      
      if ua>0 and ua<1 and ub>0 and ub<1:
        total+=1
        #print(total)
        
    
    for i in range(len(people)):
      for j in range(i+1,len(people)):
        (x1,y1),(x2,y2)=loc[people[i]],loc[people[j]]

        dist=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        if dist<50:
          total+=(1.0-(dist/50.0))
          
  for i in people:#计算角度是否过小
    #print(i)
    row=[]
    #print(len(row))
    for k in range(len(links)):
     
      if links[k][0] ==i or links[k][1] == i: 
        row.append(links[k])
    #print(len(row))
    if len(row)<2:continue
    
    else:
      for j in range(len(row)):
        for m in range(j+1,len(row)):
          (x1,y1),(x2,y2)=loc[links[j][0]],loc[links[j][1]]
          (x3,y3),(x4,y4)=loc[links[m][0]],loc[links[m][1]]
          dj=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
          dm=math.sqrt(math.pow(x4-x3,2)+math.pow(y4-y3,2))
          cos=((x2-x1)*(x4-x3)+(y2-y1)*(y4-y3))/(dj*dm)
          if cos>0.8:
            #print(cos)
            total += cos
  return total


def drawnetwork(sol,jpeg='net.jpg'):
  img=Image.new('RGB',(400,400),(255,255,255))
  draw=ImageDraw.Draw(img)

  pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])

  for (a,b) in links:
    draw.line((pos[a],pos[b]),fill=(255,0,0))

  for n,p in pos.items():
    draw.text(p,n,(0,0,0))
  
  img.save(jpeg,'JPEG')#不存怎么好比较嘛~~书本一点都不考虑用户体验~~~

  img.show()


        




domain=[(10,370)]*(len(people)*2)
#print(domain)#生成一堆位置坐标的边界值。