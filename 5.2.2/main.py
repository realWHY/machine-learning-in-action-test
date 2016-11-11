import logRegres
dataArr, labelMat = logRegres.loadDataSet()
#print('dataArr',dataArr)
#print('labelMat',labelMat)
weight = logRegres.gradAscent(dataArr, labelMat)
print('weight',weight)
