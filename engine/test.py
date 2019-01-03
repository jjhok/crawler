def solution(X, A):
    diffList = set(range(1,X+1))

    for index in range(0,len(A)):
        tmp = set(A[:index+1])
        if len(diffList - tmp) == 0:
            return index
    
    return -1



print(solution(4, [1,3,1,4,2,3,5,4]))