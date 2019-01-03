import random
import time


########### TEST CASE ##############
## 랜덤 발생
case1 = random.randint(1, 100000)
print("테스트 값 : {}".format(case1))

# # ### 리스트 (순차적)
# # case2 = list(range(-1000000, 1000001))
# # random.shuffle(case2)       # shuffle
# # # print("테스트 값 : {}".format(case2))

# ### 랜덤 리스트 / 랜덤 개
count = random.randint(1, case1)
case3 = list()
for i in range(0, case1):
    case3.append(random.randint(1, case1 + 1))
print("테스트 값 : {}개".format(count))
# print("테스트 값 : {}\n{}개".format(case3, count))



#####################################


#################   메인 함수  ####################
## 4-1
# def solution(X, A):
#     diffList = set(range(1,X+1))
#     tmp = set()
#     for index, value in enumerate(A):
#         tmp.add(value)
#         if tmp == diffList :
#             return index
#     return -1

## 4-2
# def solution(A):
#     s = sorted(A)

#     lastValue = 0
#     for value in s:
#         if value - lastValue != 1:
#             return 0
#         lastValue = value
#     return 1


## 4-3
# def solution(A):
#     positiveList = list(sorted(set(filter(lambda x: x>0, A))))
#     if len(positiveList) == 0:
#         return 1
#     for index, value in enumerate(positiveList):
#         if index + 1 != value:
#             return index + 1  
#     return positiveList[-1] + 1

## 4-4 (1)
def solution(N, A):
    result = [0] * N
    remainList = A

    idx = 0
    maxCounter = 0
    while True:
        try:
            idx = remainList.index(N+1)
        except:
            break
        tempList = remainList[:idx]
        remainList = remainList[idx+1:]

        counts = []
        for i in range(0, N+1):
            counts.append(tempList.count(i))
        maxCounter = maxCounter + max(counts)
        result = [maxCounter] * N
    
    for value in remainList:
        result[value-1] += 1
    
    return result

## 4-4 (2)
def solution(N, A):
    result = [0] * N
    for value in A:
        if value != N+1:
            result[value-1] += 1
        else:
            result = [max(result)] * N
    
    return result



#################################################


### TEST CASE
N = 5
A = [3,4,4,6,1,4,4]

# [최대, 최소], worstcase 테스트 할 것.


### 타임 측정
import time

begin = time.time()

print("--------------------------------")
print(solution(N, A))
print("--------------------------------")

end = time.time()
print("TIME Elapsed : {}".format(end-begin))