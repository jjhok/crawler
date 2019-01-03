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


