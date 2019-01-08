1번

def solution(A):
    decimal = int(A, 2)
    count = 0

    while decimal != 0:
        if decimal % 2 == 0:
            decimal = decimal / 2
        else :
            decimal -= 1
        count += 1

    return count





2번
def solution(A):
    listData = A.split("\n")
    dicts = []
    ## to dictioary object
    for index, string in enumerate(listData):
        splitted = string.split(",")
        
        position = index
        name = splitted[0].split(".")[0]
        extension = splitted[0].split(".")[-1].strip()
        city = splitted[1].strip()
        date = splitted[2].strip()

        dict = {
            'position': position,
            'name': name,
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


3번
def solution(A, B, M, X, Y):
    moveCount = 0

    totalWeight = 0
    people = 0
    targetFloors = set()
    
    while A:
        if totalWeight + A[0] <= Y and people + 1 <= X:
            totalWeight += A.pop(0)
            targetFloors.add(B.pop(0))
            people += 1

        else : 
            moveCount += len(targetFloors) + 1
            totalWeight = 0
            people = 0
            targetFloors = set()
    
    moveCount += len(targetFloors) + 1
    return moveCount


4번