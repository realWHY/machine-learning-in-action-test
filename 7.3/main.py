import adaboost
from numpy import *
'''
datMat, classLabels= adaboost.loadSimpData()
D = mat(ones((5,1))/5)
adaboost.draw(datMat,classLabels)
weakClassArr = classifyierArray = adaboost.adaBoostTrainDS(datMat, classLabels, 9)
#print('bestStump = ',bestStump)
#print('minError = ',minError)
#print('bestClasEst = ',bestClasEst)
print('weakClassArr = ',weakClassArr)
datToClass = [[5,5],[0,0]]
adaboost.adaClassify(datToClass,weakClassArr)
'''
dataMat,labelMat=adaboost.loadDataSet("horseColicTraining2.txt")
classifyierArray = adaboost.adaBoostTrainDS(dataMat, labelMat, 10)

testMat,testlabelMat=adaboost.loadDataSet("horseColicTest2.txt")
prediction = adaboost.adaClassify(testMat,classifyierArray)
print("prediction= ",prediction)
errorRate = adaboost.errorRate(testlabelMat,prediction)
print("errorRate= ",errorRate)
