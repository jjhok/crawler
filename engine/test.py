import random
import time


########### TEST CASE ##############
## 랜덤 발생
def IntRandom(minRange, maxRange):
    result = random.randint(minRange, maxRange+1)
    print("테스트 값 : {}".format(case1))
    return result

# # ### 리스트 (순차적)
def listSequence(minRange, maxRange):
    result = list(range(minRange, maxRange+1))
    return result
    print("테스트 값 : {}".format(result))


# ### 랜덤 리스트 / 랜덤 개
def ListRandom(count, minRange, maxRange):
    result = list()
    for i in range(0, count):
        result.append(random.randint(minRange, maxRange+1))
    print("테스트 값 : {}개".format(count))
    # print("테스트 값 : {}\n{}개".format(case3, count))
    return result

# shuffle
def listShuffle(list):
    return random.shuffle(list) 

#####################################


#################   메인 함수  ####################
def solution(A):
    avgs = []
    idxs = []

    idx = 0
    avg = sum(A[0:1])/len(A[0:1])
    for startIdx in range(0, len(A)-1):
        for endIdx in range(startIdx+1, len(A)):
            if A[endIdx] >= avg or sum(A[startIdx:endIdx+1])/len(A[startIdx:endIdx+1]) >= avg:
                continue
            avg = sum(A[startIdx:endIdx+1])/len(A[startIdx:endIdx+1])
            idx = startIdx
            # avgs.append(sum(A[startIdx:endIdx+1])/len(A[startIdx:endIdx+1]))
            # idxs.append(startIdx)
    
    # return idxs[avgs.index(min(avgs))]
    return idx


#################################################


### TEST CASE
A = [1000, -1000]

# [최대, 최소], worstcase 테스트 할 것.


### 타임 측정
import time

begin = time.time()

print("--------------------------------")
print(solution(A))
print("--------------------------------")

end = time.time()
print("TIME Elapsed : {}".format(end-begin))