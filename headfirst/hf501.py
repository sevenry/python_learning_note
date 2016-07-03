scores={}
result_f=open("results.txt")
for each_line in result_f:#系统对for自动从上到下来排序。
    #for 后面可以视为临时变量 所以each_line换成a，b等均可以
    (name,score)=each_line.split()
    scores[score]=name  #[]内为key的部分，name为key对应的值
result_f.close
print("the top scores were:")
for each_score in sorted(scores.keys(),reverse=True):
    print('surfer '+scores[each_score]+' scored '+each_score)

