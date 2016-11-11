import treePlotter
import tree

myDat, labels = tree.createDataSet()
labelsTemp = []
labelsTemp[:] = labels[:]
print('00000000000000000000labels = ', labelsTemp)
#myTree = tree.createTree(myDat, labelsTemp)
#tree.storeTree(myTree,'Tree.txt')
myTreeFromFile = tree.grabTree('Tree.txt')
print('myTreeFromFile = ', myTreeFromFile)
print('labels = ', labels)
result = tree.classify(myTreeFromFile, labels, [1,0])
print('result = ', result)
