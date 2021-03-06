'''
Created on Nov 28, 2010
Adaboost is short for Adaptive Boosting
@author: Peter
'''
from numpy import *
from pdb import set_trace as bp

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

def draw(datMat,labelMat):
    import matplotlib.pyplot as plt
    n = shape(datMat)[0]
    print('n =',n)
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        print('datMat[i,1]',datMat[i,0])
        print('datMat[i,2]',datMat[i,1])
        if int(labelMat[i])== 1:
            xcord1.append(datMat[i,0]); ycord1.append(datMat[i,1])
        else:
            xcord2.append(datMat[i,0]); ycord2.append(datMat[i,1])
    print('xcord1',xcord1)
    print('xcord2',xcord2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='green' )
    ax.scatter(xcord2, ycord2, s=30, c='red', marker='s')
    ax.plot()
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()
    
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields 
    print("numFeat = ",numFeat)
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
            #print("lineArr = ",lineArr)
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#just classify the data
    #print('dataMatrix = ',dataMatrix)
    #print('dimen = ',dimen)
    #print('threshVal = ',threshVal)
    #print('threshIneq = ',threshIneq)
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray
    

def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    #print('m = ',m)
    #print('n = ',n)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
    minError = inf #init error sum, to +infinity
    for i in range(n):#loop over all dimensions
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
        #print('rangeMin = ',rangeMin)
        #print('rangeMax = ',rangeMax)
        stepSize = (rangeMax-rangeMin)/numSteps
        #print('stepSize = ',stepSize)
        #print('range(-1,int(numSteps)+1) = ',range(-1,int(numSteps)+1))
        for j in range(-1,int(numSteps)+1):#loop over all range in current dimension
            for inequal in ['lt', 'gt']: #go over less than and greater than
                threshVal = (rangeMin + float(j) * stepSize)
                #print('threshVal = ',threshVal)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)#call stump classify with i, j, lessThan
                #print('predictedVals = ',predictedVals);
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                #print('errArr = ',errArr);
                weightedError = D.T*errArr  #calc total error multiplied by D
                #print("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError))
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
                    #print("bestStump['dim'] = ",bestStump['dim'])
                    #print("bestStump['thresh'] = ",bestStump['thresh'])
                    #print("bestStump['ineq'] = ",bestStump['ineq'])
    return bestStump,minError,bestClasEst


def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)   #init D to all equal
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        #print("i= ",i)
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#build Stump
        #print("D:",D.T)
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))#calc alpha, throw in max(error,eps) to account for error=0
        print("alpha: ",alpha)
        bestStump['alpha'] = alpha  
        weakClassArr.append(bestStump)                  #store Stump Params in Array
        print("classEst: ",classEst.T)
        expon = multiply(-1*alpha*mat(classLabels).T,classEst) #exponent for D calc, getting messy
        #print("expon: ",expon)
        D = multiply(D,exp(expon))                              #Calc New D for next iteration
        D = D/D.sum()
        #print("D after: ",D)
        #calc training error of all classifiers, if this is 0 quit for loop early (use break)
        aggClassEst += alpha*classEst
        print("aggClassEst: ",aggClassEst.T)
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
        print("sign(aggClassEst): ",sign(aggClassEst))
        print("sign(aggClassEst) != mat(classLabels).T: ",sign(aggClassEst) != mat(classLabels).T)
        print("aggErrors: ",aggErrors)
        errorRate = aggErrors.sum()/m
        print("total error: ",errorRate)
        if errorRate == 0.0: break
    return weakClassArr, aggClassEst

def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)#do stuff similar to last aggClassEst in adaBoostTrainDS
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix, classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])#call stump classify
        aggClassEst += classifierArr[i]['alpha']*classEst
        print("test aggClassEst",aggClassEst)
    return sign(aggClassEst)

def errorRate(testlabelMat,prediction):
    errArr = ones((shape(testlabelMat)[0],1))
    #print("errArr",errArr)
    #print(mat(prediction)!=mat(testlabelMat).T)
    errCount = errArr[mat(prediction)!=mat(testlabelMat).T].sum()
    errorRate =errCount/errArr.sum()
    return errorRate
    
def plotROC(predStrengths, classLabels):
    import matplotlib.pyplot as plt
    print("predStrengths = ",predStrengths)
    print("classLabels = ",classLabels)
    cur = (1.0,1.0) #cursor
    ySum = 0.0 #variable to calculate AUC
    numPosClas = sum(array(classLabels)==1.0)
    print("numPosClas = ",numPosClas)
    yStep = 1/float(numPosClas); xStep = 1/float(len(classLabels)-numPosClas)
    print("xStep = %f,  yStep = %f= "%(xStep,yStep))
    sortedIndicies = predStrengths.argsort()#get sorted index, it's reverse
    print("sortedIndicies = ",sortedIndicies)
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    #loop through all the values, drawing a line segment at each point
    for index in sortedIndicies.tolist()[0]:
        print("index = ",index)
        if classLabels[index] == 1.0:
            delX = 0; delY = yStep;
        else:
            delX = xStep; delY = 0;
            ySum += cur[1]
        #draw line from cur to (cur[0]-delX,cur[1]-delY)
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')
        cur = (cur[0]-delX,cur[1]-delY)
        print(cur)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
    plt.title('ROC curve for AdaBoost horse colic detection system')
    ax.axis([0,1,0,1])
    plt.show()
    print("the Area Under the Curve is: ",ySum*xStep)
