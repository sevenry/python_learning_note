def find_details(id2find):
    surfers_f=open('surfing_data.txt')
    for each_line in surfers_f:
        s={}
        (s['id'],s['name'],s['country'],s['average'],s['board'],s['age'])=each_line.split(";")
        if id2find==int(s['id']):
            surfers_f.close()
            return(s)
    surfers_f.close()
    return({})

lookup_id=int(input("enter the id of the surfer: "))
surfer=find_details(lookup_id)#此处定义了surfer，所以下面的注明不应该是s，而是surfer
#sufer利用函数 找到对应id的数据 函数处理了数据 对每一个对应的数据的key赋值是在surfer里完成
if surfer:
    print("ID:       "+surfer['id'])
    print("Name:     "+surfer['name'])
    print("Country:  "+surfer['country'])
    print("Average:  "+surfer['average'])
    print("Board:    "+surfer['board'])
    print("Age:      "+surfer['age'])
