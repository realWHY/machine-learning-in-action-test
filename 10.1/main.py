import kMeans
from numpy import *

datMat = mat(kMeans.loadDataSet('testSet2.txt'))
print('datMat = ',datMat)

#centroids = kMeans.randCent(datMat, 2)
#print('centroids = ',centroids)
#centroids, clusterAssment = kMeans.biKmeans(datMat, 3)
#kMeans.Draw(datMat, centroids)
distance = kMeans.clusterClubs()
