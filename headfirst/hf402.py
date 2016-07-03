highest_score=0
second_score=0
third_score=0
result_f=open("results.txt")
for each_line in result_f:
    (name,score)=each_line.split()
    if float(score)>third_score:
        if float(score)>second_score:
            if float(score)>highest_score:
                highest_score=float(score)
            else:
                second_score=float(score)
        else:
            third_score=float(score)
result_f.close()
print("the highest score is:")
print(highest_score)
print("the second score is:")
print(second_score)
print("the third score is:")
print(third_score)


