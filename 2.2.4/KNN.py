from numpy import *
import operator

def createDataSet():
	group = array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
	labels = ['A','A','B','B']
	print("group = ",group)
	print("labels = ",labels)
	return group, labels

def classify0(intX, dataSet, labels, k):
        datasetSize = dataSet.shape[0]
        #print("datasetSize = ",datasetSize)
        diffMat = tile(intX, (datasetSize,1))-dataSet
        #print("diffMat = ",diffMat)
        sqDiffMat = diffMat**2
        #print("sqDiffMat = ",sqDiffMat)
        sqDistances = sqDiffMat.sum(axis=1)
        #print("sqDistances = ",sqDistances)
        distances = sqDistances**0.5
        #print("distances = ",distances)
        sortedDistIndicies = distances.argsort()
        #print("sortedDistIndicies = ",sortedDistIndicies)
        ClassCount={}
        for i in range(k):
                voteIlabel = labels[sortedDistIndicies[i]]
                #print("voteIlabel = ",voteIlabel)
                ClassCount[voteIlabel] = ClassCount.get(voteIlabel,0)+1
                #print("ClassCount = ",ClassCount)
        sortedClassCount = sorted(ClassCount.items(),
                                  key=operator.itemgetter(1), reverse=True)
        #print("sortedClassCount = ",sortedClassCount)
        #print("sortedClassCount[0][0] = ",sortedClassCount[0][0])
        return sortedClassCount[0][0]

def file2matrix(filename):
        fr = open(filename)
        numberOfLines = len(fr.readlines())
        print("numberOfLines = ",numberOfLines)
        returnMat = zeros((numberOfLines,3))
        print("returnMat = ",returnMat)
        classLabelVector = []
        fr = open(filename)
        index = 0
        
        for line in fr.readlines():
                line = line.strip()
                love_dictionary={'largeDoses':3, 'smallDoses':2, 'didntLike':1}
                listFromLine = line.split('\t')
                returnMat[index,:] = listFromLine[0:3]
                if(listFromLine[-1].isdigit()):
                    classLabelVector.append(int(listFromLine[-1]))
                else:
                    classLabelVector.append(love_dictionary.get(listFromLine[-1])) 
                index += 1
        return returnMat, classLabelVector

def autoNorm(dataSet):
        print("--------------start to normalize data --------------")
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        print("dataSet.max(0) = ",dataSet.max(0))
        print("dataSet.min(0) = ",dataSet.min(0))
        ranges = maxVals - minVals
        print("ranges = ",ranges)
        print("shape(dataSet) = ",shape(dataSet))
        normDataSet = zeros(shape(dataSet))
        m = dataSet.shape[0]
        print("m = ",m)
        print("tile(minVals, (m,1) = ",tile(minVals, (m,1)))
        normDataSet = dataSet - tile(minVals, (m,1))
        normDataSet = normDataSet/tile(ranges, (m,1))
        print("normDataSet = ",normDataSet)
        return normDataSet, ranges, minVals

def datingClassTest():
        hoRatio = 0.1      #hold out 10%
        datingDataMat,datingLabels = file2matrix('datingTestSet.txt')       #load data setfrom file
        normMat, ranges, minVals = autoNorm(datingDataMat)
        m = normMat.shape[0]
        numTestVecs = int(m*hoRatio)
        errorCount = 0.0
        for i in range(numTestVecs):
                classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],4)
                print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
                if (classifierResult != datingLabels[i]): errorCount += 1.0
        print("errorCount:",errorCount)
        print("the total error rate is: %f" % (errorCount/float(numTestVecs)))

def classifyPerson():
        resultList = ['not at all', 'in small doses', 'in large doses']
        percentTats = float(input(\
                "percentage of time spent playing video games?"))
        ffMiles = float(input("frequent flier miles earned per year?"))
        iceCream = float(input("liters of ice cream consumed per year?"))
        datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
        normMat, ranges, minVals = autoNorm(datingDataMat)
        inArr = array([ffMiles, percentTats, iceCream, ])
        classifierResult = classify0((inArr - \
                                      minVals)/ranges, normMat, datingLabels, 3)
        print("You will probably like this person: %s" % resultList[classifierResult - 1])
