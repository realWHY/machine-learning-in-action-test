import KNN

group, labels = KNN.createDataSet()
intX = [0.6,0.6]
k = 3
KNN.classify0(intX, group, labels, k)
