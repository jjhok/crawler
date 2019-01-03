import random
import time


########### TEST CASE ##############
## 랜덤 발생
case1 = random.randint(1, 1000000)
print("테스트 값 : {}".format(case1))

### 리스트 (순차적)
# case2 = list(range(-1000, 1001))
# print("테스트 값 : {}".format(case2))

### 랜덤 리스트 / 랜덤 개
count = random.randint(1, case1)
case3 = list()
for i in range(0, count):
    case3.append(random.randint(1, 1000000))
print("테스트 값 : {}개".format(count))
# print("테스트 값 : {}\n{}개".format(case3, count))
#####################################


#################   메인 함수  ####################
def solution(X, A):
    diffList = set(range(1,X+1))
    tmp = set()
    for index, value in enumerate(A):
        tmp.add(value)
        if tmp == diffList :
            return index
    
    
    return -1
#################################################


### TEST CASE
X = 5
A = [1,3,1,4,2,3,5,4]

# [최대, 최소], worstcase 테스트 할 것.


### 타임 측정
import time

begin = time.time()

print("--------------------------------")
print(solution(case1, case3))
print("--------------------------------")

end = time.time()
print("TIME Elapsed : {}".format(end-begin))