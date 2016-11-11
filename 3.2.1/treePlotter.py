
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.9")
leafNode = dict(boxstyle="round4", fc="0.5")
arrow_args = dict(arrowstyle="<|-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='data',
             xytext=centerPt, textcoords='data',
             verticalalignment='center', horizontalalignment='center', bbox=nodeType, arrowprops=arrow_args )
'''
def createPlot():
    fig = plt.figure(1, facecolor='0.9')
    fig.clf()
    createPlot.ax1 = plt.subplot(111) #ticks for demo puropses 
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
'''

def getNumLeafs(myTree):
    print('-------------start getNumLeafs----------------')
    numLeafs = 0
    print('myTree.keys()[0]', list(myTree.keys())[0])
    print('type(list(myTree.keys())[0]) = ', type(list(myTree.keys())[0]))
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    print('secondDict',secondDict)
    for key in secondDict.keys():
        print('key',key)
        print('secondDict[key] = ',secondDict[key])
        print('type(secondDict[key]).__name__ = ',type(secondDict[key]).__name__)
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs +=1
        print('numLeafs = ',numLeafs)
    print('-------------end getNumLeafs----------------')
    return numLeafs

def getTreeDepth(myTree):
    print('-------------start getTreeDepth----------------')
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    print('myTree.keys()[0]', list(myTree.keys())[0])
    print('type(list(myTree.keys())[0]) = ', type(list(myTree.keys())[0]))
    secondDict = myTree[firstStr]
    print('secondDict',secondDict)
    for key in secondDict.keys():
        print('key',key)
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    print('-------------end getTreeDepth----------------')
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]    #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    print('cntrPt= ',cntrPt)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes   
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
#if you do get a dictonary you know it's a tree, and the first element will be another dict

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[0,1,2], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    print('plotTree.xOff= ',plotTree.xOff)
    plotTree(inTree, (0.1,0.7), 'This is Tree')
    plt.show()

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel
