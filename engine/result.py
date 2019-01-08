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
# def solution(N, A):
#     result = [0] * N
#     remainList = A

#     idx = 0
#     maxCounter = 0
#     while True:
#         try:
#             idx = remainList.index(N+1)
#         except:
#             break
#         tempList = remainList[:idx]
#         remainList = remainList[idx+1:]

#         counts = []
#         for i in range(0, N+1):
#             counts.append(tempList.count(i))
#         maxCounter = maxCounter + max(counts)
#         result = [maxCounter] * N
    
#     for value in remainList:
#         result[value-1] += 1
    
#     return result

# ## 4-4 (2)
# def solution(N, A):
#     result = [0] * N
#     for value in A:
#         if value != N+1:
#             result[value-1] += 1
#         else:
#             result = [max(result)] * N
    
#     return result


# # 5-1 (1) : 50%
# def solution(A):
#     result = 0
#     for index, value in enumerate(A):
#         if value == 0:
#             result += A[index:].count(1)
#             if result > 1000000000:
#                 return -1
#     return result

# # 5-1 (2) : 100%
# def solution(A):
#     zeroCount = 0
#     result = 0

#     for value in A:
#         if value == 0:
#             zeroCount += 1
#         else :
#             result += zeroCount
    
#         if result > 1000000000:
#             return -1
#     return result


# # 5-2 : 62% 성능부족
# def solution(S, P, Q):
#     strList = list(S)
#     resultStrList = []
#     for index in range(0, len(P)):
#         start = P[index]
#         end = Q[index]
#         resultStrList.append(min(strList[start:end+1]))
    
#     for index, char in enumerate(resultStrList):
#         if char == 'A':
#             resultStrList[index] = 1
#         elif char == 'C':
#             resultStrList[index] = 2
#         elif char == 'G':
#             resultStrList[index] = 3
#         elif char == 'T':
#             resultStrList[index] = 4
    
#     return resultStrList


## 5-4 
# def solution(A, B, K):
#     import math
#     first = math.ceil(A/K) * K
#     last = math.floor(B/K) * K
#     innerCount = (last - first) / K - 1

#     return int(innerCount + 2)


## 6-1
# def solution(A):
#     return len(set(A))

# # 6-2
# def solution(A):
#     A.sort()
#     minusMax = A[0] * A[1]
#     A.reverse()
#     plusMax = A[0] * A[1] * A[2]
#     return max([minusMax * A[0], plusMax])

# # 6-3
# def solution(A):
#     A.sort()
#     filtered = list(filter(lambda x: x>0, A))
#     for index in range(0, len(filtered)-2):
#         if filtered[index] + filtered[index+1] > filtered[index+2]:
#             return 1  
#     return 0

# 6-4: 50% 성능포기
# def solution(A):
#     leftPoints = []
#     rightPoints = []
#     for index, value in enumerate(A):
#         leftPoints.append(index - value)
#         rightPoints.append(index + value)
    
#     leftSideOutCount = 0
#     rightSideOutCount = 0
#     for index in range(0, len(A)):
#         leftSideOutCount += len(list(filter(lambda x: x < leftPoints[index], rightPoints[index+1:])))
#         rightSideOutCount += len(list(filter(lambda x: x > rightPoints[index], leftPoints[index+1:])))

#     return totalChance(len(A)) - leftSideOutCount - rightSideOutCount

# def totalChance(count):
#     if count == 0: 
#         return 0
#     else :
#         return count - 1 + totalChance(count - 1)


# # 7-1
# def solution(A):
#     if len(A) == 0:
#         return 1

#     stk = list(A)
#     tmp = ['']
    
#     while stk:
#         target = stk.pop()

#         pair = getPair(tmp[-1])
#         if target == pair:
#             tmp.pop()
#         else:
#             tmp.append(target)

#     if tmp == [''] :
#         return 1
#     else:
#         return 0

# def getPair(C):
#     if C == "]":
#         return "["
#     if C == "}":
#         return "{"
#     if C == ")":
#         return "("


# # 7-2
# def solution(A, B):
#     downfishes = []
#     remain = 0

#     for index in range(0, len(A)):
#         if B[index] == 0:
#             while len(downfishes) > 0 and  downfishes[-1] < A[index]:
#                     downfishes.pop()

#             if len(downfishes) == 0:
#                 remain += 1
                
#         else :
#             downfishes.append(A[index])
    
#     return remain + len(downfishes)


# # 8-1 : 55%
# def solution(A):
#     result = 0
#     for splitIndex in range(1, len(A)):
#         left = A[:splitIndex]
#         right = A[splitIndex: len(A)]

#         leftLeader = getLeader(left)
#         if leftLeader == -1:
#             continue

#         rightLeader = getLeader(right)
#         if rightLeader == -1:
#             continue

#         if leftLeader == rightLeader :
#             result += 1

#     return result


# def getLeader(array):
#     countDict = {}
#     for value in array:
#         try:
#             countDict[value] += 1
#         except:
#             countDict[value] = 1
        
#         if countDict[value] > len(array)/2 :
#             return value
#     return -1


# # 8-2
# def solution(A):
#     countDict = {}
#     for index, value in enumerate(A):
#         try:
#             countDict[value] += 1
#         except:
#             countDict[value] = 1
#         if countDict[value] > len(A)/2 :
#             return index
#     return -1
