import pandas as pd
import sys
import json


def printCombination(arr, n, r):
    data = [0]*r
    combinationUtil(arr, data, 0, n - 1, 0, r)


def combinationUtil(arr, data, start, end, index, r):
    global combinations
    if (index == r):
        combi = []
        for j in range(r):
            combi.append(data[j])

        x = "and".join(combi)
        combinations.append(x)

        return
    i = start
    while(i <= end and end - i + 1 >= r - index):
        data[index] = arr[i]
        combinationUtil(arr, data, i + 1, end, index + 1, r)
        i += 1


def Pairs(value):
    if "And" in value:
        z = 0
        if "NS," in value:
            z = 1
            value = value.replace("NS,", "")

        alist = value.split('And')
        n = len(alist)
        global combinations
        combinations = []
        for i in range(1, n+1):
            printCombination(alist, n, i)
        result = ",".join(combinations)
        if z == 1:
            return "NS,"+result
        else:
            return result
    else:
        return value


data = json.loads(sys.argv[1])

df = pd.DataFrame(data, index=None)
df['values'] = df['values'].apply(Pairs)

uData = df.to_dict(orient='records')
uData = json.dumps(uData)
print(uData)
