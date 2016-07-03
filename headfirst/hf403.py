scores=[]
result_f=open("results.txt")
for each_line in result_f:
    (name,score)=each_line.split()
    scores.append(float(score))
result_f.close
scores.sort()
scores.reverse()
print("the top scores were:")
print(scores[0])
print(scores[1])
print(scores[2])
