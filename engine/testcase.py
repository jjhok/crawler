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
    listData = A.split("\n")
    dicts = []
    ## to dictioary object
    for index, string in enumerate(listData):
        splitted = string.split(",")
        
        position = index
        extension = splitted[0].split(".")[-1].strip()
        city = splitted[1].strip()
        date = splitted[2].strip()

        dict = {
            'position': position,
            'extension': extension,
            'city': city,
            'date': date,
        }
        
        dicts.append(dict)

    ## city 별로 split
    cities = {}

    for dict in dicts:
        try:
            cities[dict['city']].append(dict)
        except:
            cities[dict['city']] = [dict]
    
    names = []
    for city in cities.values():
        orderedCity = ordering(city)
        names += generateName(orderedCity)

    originalPositionDicts = sorted(names, key=lambda k: k['position'])
    
    return '\n'.join([dic['newName'] for dic in originalPositionDicts])

# add index 
def ordering(dicList):
    sortedList = sorted(dicList, key=lambda k: k['date']) 
    for index, dic in enumerate(sortedList):
        dic['index'] = index + 1
    return dicList

#add newName
def generateName(indexedDicList):
    newDicts = indexedDicList
    for dic in newDicts:
        if len(newDicts) < 10:
            dic['newName'] = "{}{}.{}".format(dic['city'], dic['index'], dic['extension'])
        elif 10 <= len(newDicts) < 100:
            dic['newName'] = "{0}{1:02d}.{2}".format(dic['city'], dic['index'], dic['extension'])
        else :
            dic['newName'] = "{0}{1:03d}.{2}".format(dic['city'], dic['index'], dic['extension'])
    return newDicts


 

#################################################


### TEST CASE
# count = intRandom(0, 10000)
# A = listRandom(count, 0, 2147483647)


A = "000011110100001001000000"
B = [3,3,2,2,3]
M = 1
X = 90
Y = 200


# [최대, 최소], worstcase 테스트 할 것.


### 타임 측정
import time

begin = time.time()

print("--------------------------------")
print(solution(A))
print("--------------------------------")

end = time.time()
print("TIME Elapsed : {}".format(end-begin))