from numpy import *
import operator

def createDataSet():
	group = array([[1.0,1.1], [0,0], [0,0.1], [1.0,1.0]])
	labels = ['A','B','B','A']
	print("group = ",group)
	print("labels = ",labels)
	return group, labels

def classify0(intX, dataSet, labels, k):
        datasetSize = dataSet.shape[0]
        print("datasetSize = ",datasetSize)
        diffMat = tile(intX, (datasetSize,1))-dataSet
        print("diffMat = ",diffMat)
        sqDiffMat = diffMat**2
        print("sqDiffMat = ",sqDiffMat)
        sqDistances = sqDiffMat.sum(axis=1)
        print("sqDistances = ",sqDistances)
        distances = sqDistances**0.5
        print("distances = ",distances)
        sortedDistIndicies = distances.argsort()
        print("sortedDistIndicies = ",sortedDistIndicies)
        ClassCount={}
        for i in range(k):
                voteIlabel = labels[sortedDistIndicies[i]]
                print("voteIlabel = ",voteIlabel)
                ClassCount[voteIlabel] = ClassCount.get(voteIlabel,0)+1
                print("ClassCount = ",ClassCount)
        sortedClassCount = sorted(ClassCount.items(),
                                  key=operator.itemgetter(1), reverse=True)
        print("sortedClassCount = ",sortedClassCount)
        print("sortedClassCount[0][0] = ",sortedClassCount[0][0])
        return sortedClassCount[0][0]
