import regTrees
from numpy import *
'''
testMat = mat(eye(4))
print('testMat',testMat)
mat0,mat1 = regTrees.binSplitDataSet(testMat,1,0.5)
print('mat0 = ',mat0)
print('mat1 = ',mat1)
'''
#--------------------------------------------
myDat = regTrees.loadDataSet('ex00.txt')
myMat = mat(myDat)
print('myMat = ',myMat)
retTree = regTrees.createTree(myMat)
print('retTree = ',retTree)
