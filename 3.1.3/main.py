import tree

myDat, labels = tree.createDataSet()
print('myDat = ',myDat)
print('labels = ',labels)
myTree = tree.createTree(myDat, labels)
