'''
Created on Oct 19, 2010

@author: Peter
'''
from numpy import *
from pdb import set_trace as bp
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec
                 
def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        #print('document= ',document)
        vocabSet = vocabSet | set(document) #union of the two sets
        #print('vocabSet= ',vocabSet)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    print('inputSet= ',inputSet)
    print('vocabList= ',vocabList)
    returnVec = [0]*len(vocabList)
    print('returnVec= ',returnVec)
    for word in inputSet:
        print('word= ',word)
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print("the word: %s is not in my Vocabulary!" % word)
    #print('return returnVec= ',returnVec)
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    print("-----start trainNB0 ----- ")
    numTrainDocs = len(trainMatrix)
    print("numTrainDocs = ", numTrainDocs)
    numWords = len(trainMatrix[0])
    print("trainMatrix[0] = ", trainMatrix[0])
    print("numWords = ", numWords)
    print("sum(trainCategory) = ", sum(trainCategory))
    print("float(numTrainDocs) = ", float(numTrainDocs))
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    print("pAbusive = ", pAbusive)
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        print("i = ", i)
        print("trainCategory[i] = ", trainCategory[i])
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            print("p1Num = ", p1Num)
            p1Denom += sum(trainMatrix[i])
            print("p1Denom = ", p1Denom)
        else:
            p0Num += trainMatrix[i]
            print("p0Num = ", p0Num)
            p0Denom += sum(trainMatrix[i])
            print("p0Denom = ", p0Denom)
    p1Vect = log(p1Num/p1Denom)      #change to log()
    print("p1Vect = ", p1Vect)
    p0Vect = log(p0Num/p0Denom)         #change to log()
    print("p0Vect = ", p0Vect)
    print("-----end trainNB0 ----- ")
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    print("p1 = ", p1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    print("p0 = ", p0)
    if p1 > p0:
        return 1
    else: 
        return 0
    
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        #print('returnVec = ',returnVec)
    return returnVec

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb))

def textParse(bigString):    #input is big string, #output is word list
    import re
    #print('bigString = ',bigString)
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] 
    
def spamTest():
    docList=[]; classList = []; fullText =[]
    rmax = 25
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i,'rb').read())
        #print('spam wordList = ',wordList)
        docList.append(wordList)
        #print('spam docList = ',docList)
        fullText.extend(wordList)
        #print('spam fullText = ',fullText)
        classList.append(1)
        #print('spam classList = ',classList)
        wordList = textParse(open('email/ham/%d.txt' % i,'rb').read())
        #print('ham wordList = ',wordList)
        docList.append(wordList)
        #print('ham docList = ',docList)
        fullText.extend(wordList)
        #print('ham fullText = ',fullText)
        classList.append(0)
        #print('ham classList = ',classList)
    print('wordList = ',wordList)
    print('docList = ',docList)
    print('fullText = ',fullText)
    print('classList = ',classList)
    vocabList = createVocabList(docList)#create vocabulary
    print('vocabList = ',vocabList)  
    trainingSet = list(range(50)); testSet=[]           #create test set
    for i in range(10):
        #print('len(trainingSet) = ',len(trainingSet))  
        randIndex = int(random.uniform(0,len(trainingSet)))
        #print('randIndex = ',randIndex)  
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    print('testSet = ',testSet)  
    print('trainingSet = ',trainingSet)
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        #print('trainMat = ',trainMat)
        trainClasses.append(classList[docIndex])
        #print('trainClasses = ',trainClasses)
    print('trainMat = ',trainMat)
    print('trainClasses = ',trainClasses)
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print("classification error",docList[docIndex])
    print('the error rate is: ',float(errorCount)/len(testSet))
    #return vocabList,fullText

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    #print('freqDict',freqDict)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True) 
    #print('sortedFreq',sortedFreq)
    return sortedFreq[:30]       

def localWords(feed1,feed0):
    import feedparser
    docList=[]; classList = []; fullText =[]
    print("len(feed1['entries'] = ",len(feed1['entries']))
    print("len(feed0['entries'] = ",len(feed0['entries']))
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    print("minLen = ",minLen)
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        #print("wordList = ",wordList)
        docList.append(wordList)
        #print("docList = ",docList)
        fullText.extend(wordList)
        #print("fullText = ",fullText)
        classList.append(1) #NY is class 1
        #print("classList = ",classList)
        wordList = textParse(feed0['entries'][i]['summary'])
        #print("wordList = ",wordList)
        docList.append(wordList)
        #print("docList = ",docList)
        fullText.extend(wordList)
        #print("fullText = ",fullText)
        classList.append(0)
        #print("classList = ",classList)
    #print('wordList = ',wordList)
    #print('docList = ',docList)
    #print('fullText = ',fullText)
    #print('classList = ',classList)
    vocabList = createVocabList(docList)#create vocabulary
    top30Words = calcMostFreq(vocabList,fullText)   #remove top 30 words
    #print('top30Words',top30Words)
    #bp()
    #for pairW in top30Words:
    #    print('pairW',pairW)
    #    if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = list(range(2*minLen)); testSet=[]           #create test set
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print('the error rate is: ',float(errorCount)/len(testSet))
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[0], reverse=True)
    print('sortedSF: ',sortedSF)
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**")
    for item in sortedSF:
        print(item[0])
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**")
    for item in sortedNY:
        print(item[0])
