scores=[]
result_f=open("results.txt")
for each_line in result_f:
    (name,score)=each_line.split()
    scores.append(float(score))
result_f.close
scores.remove()# 去除某个具体的值
scores.sort()
scores.reverse()
#scores.insert(index,object)需要确定插入值的索引位置
#scores.index()表示返回的是 first index of value
#scores.extend()以元素为中心来添加，append()是作为一组整体添加
print("the top scores were:")
print(scores[0])
print(scores[1])
print(scores[2])
print(scores[3])
print(scores[4])
print(scores[5])
print("the times:")
print(scores.count(8.65))
