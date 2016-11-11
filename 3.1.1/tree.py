from math import log
import operator

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    print('numEntries = ',numEntries)
    labelCounts = {}
    print('-------------------------------------------------------')
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        print('labelCounts = ',labelCounts)
    print('-------------------------------------------------------')
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        print('prob = ',prob)
        shannonEnt -= prob * log(prob,2) #log base 2
        print('prob * log(prob,2) = ',prob * log(prob,2))
        print('shannonEnt = ',shannonEnt)
    return shannonEnt

