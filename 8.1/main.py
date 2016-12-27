import regression
from numpy import *
#dataMat,labelMat = regression.loadDataSet('ex0.txt')
#print('dataMat = ',dataMat)
#print('labelMat = ',labelMat)
#ws = regression.standRegres(dataMat, labelMat)
#print('ws = ',ws)
#regression.draw(dataMat, labelMat,ws)
#------------------------------------------------------
#xArr, yArr = regression.loadDataSet('ex0.txt')
#yHat = regression.lwlrTest(xArr, xArr, yArr, 0.01)
#regression.draw2(xArr, yArr, yHat)
#------------------------------------------------------
'''
abX,abY = regression.loadDataSet('abalone.txt')
#print(abX)
yHat01 = regression.lwlrTest(abX[0:99], abX[0:99], abY[0:99], 0.1)
yHat1 = regression.lwlrTest(abX[0:99], abX[0:99], abY[0:99], 1)
yHat10 = regression.lwlrTest(abX[0:99], abX[0:99], abY[0:99], 10)

Err0r01 = regression.rssError(abY[0:99],yHat01.T)
Err0r1 = regression.rssError(abY[0:99],yHat1.T)
Err0r10 = regression.rssError(abY[0:99],yHat10.T)

print('Err0r01 = ',Err0r01)
print('Err0r1 = ',Err0r1)
print('Err0r10 = ',Err0r10)
'''
#------------------------------------------------------

abX,abY = regression.loadDataSet('abalone.txt')
ridgeWeights = regression.ridgeTest(abX,abY)
#StandWeights =regression.standRegres(abX, abY)
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(ridgeWeights)
plt.show()

#------------------------------------------------------
'''
xArr,yArr = regression.loadDataSet('abalone.txt')
#print('xArr = ',xArr)
#print('yArr = ',yArr)
regression.stageWise(xArr,yArr)
'''
