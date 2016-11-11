import KNN
from numpy import *
import matplotlib
import matplotlib.pyplot as plt

datingDateMat, datingLabels = KNN.file2matrix('datingTestSet.txt')
print("datingDateMat = ",datingDateMat)
print("datingLabels = ",datingLabels[0:20])
normMat, ranges, minVals = KNN.autoNorm(datingDateMat)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDateMat[:,0], datingDateMat[:,1],
           15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()


