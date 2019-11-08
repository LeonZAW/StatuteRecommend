def InsertTest(myList,num):
    length = len(myList)

    temp = num
    j = length - 1
    return myList[j][1] > temp

def InsertSortItem(myList,tuple):
    length = len(myList)

    temp = tuple[1]
    j = length-1
    if myList[j][1] <= temp:
        return
    j = j-1
    while j >= 0 and myList[j][1] > temp:
        myList[j + 1] = myList[j]
        j = j - 1
    myList[j + 1] = tuple
    return
