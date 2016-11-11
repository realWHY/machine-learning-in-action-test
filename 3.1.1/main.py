import tree

myDat, labels = tree.createDataSet()
print('myDat = ',myDat)
print('labels = ',labels)
ShannonEnt = tree.calcShannonEnt(myDat)
print('ShannonEnt = ',ShannonEnt)
