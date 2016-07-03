highest_score=0
result_f=open("results.txt")
for each_line in result_f:
    (name,score)=each_line.split()
    if float(score)>highest_score:
        highest_score=float(score)
result_f.close()
print("the highest score is:")
print(highest_score)
