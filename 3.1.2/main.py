import tree

myDat, labels = tree.createDataSet()
print('myDat = ',myDat)
print('labels = ',labels)
ShannonEnt = tree.calcShannonEnt(myDat)
print('ShannonEnt = ',ShannonEnt)
splitData = tree.splitDataSet(myDat,0,1)
print('splitData = ',splitData)
BestFeature = tree.chooseBestFeatureToSplit(myDat)
print('BestFeature = ',BestFeature)
