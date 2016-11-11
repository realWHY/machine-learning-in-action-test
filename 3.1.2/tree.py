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
        #print('shannonEnt = ',shannonEnt)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:0]     #chop out axis used for splitting
            #print('reducedFeatVec = ',reducedFeatVec)
            reducedFeatVec.extend(featVec[axis+1:])
            #print('featVec[axis+1:] = ',featVec[axis+1:])
            #print('reducedFeatVec = ',reducedFeatVec)
            retDataSet.append(reducedFeatVec)
            #print('retDataSet = ',retDataSet)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    print(' -----start chooseBestFeatureToSplit------')
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels
    print('numFeatures = ',numFeatures)
    baseEntropy = calcShannonEnt(dataSet)
    print('baseEntropy = ',baseEntropy)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #iterate over all the features
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        print('featList = ',featList)
        uniqueVals = set(featList)       #get a set of unique values
        print('uniqueVals = ',uniqueVals)
        newEntropy = 0.0
        for value in uniqueVals:
            print('value = ',value)
            subDataSet = splitDataSet(dataSet, i, value)
            print('subDataSet = ',subDataSet)
            prob = len(subDataSet)/float(len(dataSet))
            print('prob = ',prob)
            newEntropy += prob * calcShannonEnt(subDataSet)
            print('newEntropy = ',newEntropy)
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
        print('bestInfoGain = ',bestInfoGain)
        print('bestFeature = ',bestFeature)
    return bestFeature                      #returns an integer
