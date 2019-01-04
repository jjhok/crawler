import random
import time


########### TEST CASE ##############
## 랜덤 발생
def intRandom(minRange, maxRange):
    result = random.randint(minRange, maxRange+1)
    print("테스트 값 : {}".format(result))
    return result

# # ### 리스트 (순차적)
def listSequence(minRange, maxRange):
    result = list(range(minRange, maxRange+1))
    return result
    print("테스트 값 : {}".format(result))


# ### 랜덤 리스트 / 랜덤 개
def listRandom(count, minRange, maxRange):
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
    if len(A) % 2 == 1: 
        return 0

    strList = list(A)
    # pairs = ["{", "}", "[", "]", "(", ")"]
    opener = ["{", "[", "("]
    closer = ["}", "]", ")"]
    stack = []

    while len(strList) > 0:
        char = strList.pop(0)
        if char in opener:
            stack.append(char)
        else : 
            stack.pop()
    return 1



#################################################


### TEST CASE
# count = intRandom(0, 10000)
# A = listRandom(count, 0, 2147483647)


A = "({{({}[]{})}}[]{})"
B = 10
K = 1

# [최대, 최소], worstcase 테스트 할 것.


### 타임 측정
import time

begin = time.time()

print("--------------------------------")
print(solution(A))
print("--------------------------------")

end = time.time()
print("TIME Elapsed : {}".format(end-begin))