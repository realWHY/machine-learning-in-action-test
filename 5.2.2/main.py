import logRegres
from numpy import *
dataArr, labelMat = logRegres.loadDataSet()
#print('dataArr',dataArr)
#print('labelMat',labelMat)
#weight = logRegres.stocGradAscent1(array(dataArr), labelMat)
logRegres.colicTest()
#print('weight',weight)
#logRegres.plotBestFit(weight)
 
