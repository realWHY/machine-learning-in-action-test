'''
Created on Feb 16, 2011
k Means Clustering for Ch10 of Machine Learning in Action
@author: Peter Harrington
'''
from numpy import *
from pdb import set_trace as bp

def Draw(datMat, centroids):
    import matplotlib.pyplot as plt
    m, n = shape(datMat)
    #print('m=%d, n =%d'%(m,n))
    xCord = []; yCord = []
    xCord = datMat[:,0]
    yCord = datMat[:,1]
    xCordCentroids = []; yCordCentroids = []
    xCordCentroids = centroids[:,0]
    yCordCentroids = centroids[:,1]
    #print('xCord = ',xCord)
    #print('yCord = ',yCord)
    #print('xCordCentroids = ',xCordCentroids)
    #print('yCordCentroids = ',yCordCentroids)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xCord, yCord, s =30, c='blue')
    ax.scatter(xCordCentroids, yCordCentroids, s =190, c='red',marker='*')
    ax.plot()
    plt.show()
    
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float,curLine)) #map all elements to float()
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    print(' n = ',n),
    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        print(' dataSet[:,j] = ',dataSet[:,j]),
        minJ = min(dataSet[:,j]) 
        rangeJ = float(max(dataSet[:,j]) - minJ)
        #print('rangeJ = ',rangeJ)
        #print('random.rand(k,1) = ',random.rand(k,1))
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
        #print('centroids[:,j] = ',centroids[:,j])
    return centroids
    
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points 
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                #print('i=%d, j =%d '%(i,j))
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                #print('distJI = ',distJI)
                if distJI < minDist:
                    minDist = distJI; minIndex = j
                    #print('minDist = ',minDist)
                    #print('minIndex = ',minIndex)
            #print('clusterAssment[i,0] = ',clusterAssment[i,0])
            #print('minIndex = ',minIndex)
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
            #print('clusterAssment[i,:] = ',clusterAssment[i,:])
        #print('clusterAssment = ',clusterAssment)
        print(centroids)
        for cent in range(k):#recalculate centroids
            #print('cent = ',cent)
            #print('nonzero(clusterAssment[:,0].A==cent)[0]',nonzero(clusterAssment[:,0].A==cent)[0])
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            #print('ptsInClust = ',ptsInClust)
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
            #print('centroids[cent,:] = ',centroids[cent,:])
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #create a list with one centroid
    #print('centList1 = ',centList)
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    #print(clusterAssment)
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
            #print('ptsInCurrCluster = ',ptsInCurrCluster)
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            #print('centroidMat = ',centroidMat)
            #print('splitClustAss = ',splitClustAss)     
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            #print('sseSplit = ',sseSplit)
            #print('sseNotSplit = ',sseNotSplit)
            #print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
            #bp()
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
                #print('nonzero(bestClustAss[:,0].A == 1)[0]= ',nonzero(bestClustAss[:,0].A == 1)[0])
        #print('bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = ',bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0])
        #print('centList = ',centList)
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        #print('len(centList): ',len(centList))
        #print('bestCentToSplit: ',bestCentToSplit)
        #print('bestClustAss: ',bestClustAss)
        #print('the bestCentToSplit is: ',bestCentToSplit)
        #print('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids 
        #print('bestNewCents: ',bestNewCents)
        #print('centList = ',centList)
        centList.append(bestNewCents[1,:].tolist()[0])
        #print('centList = ',centList)
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
        #Draw(dataSet, mat(centList))
    return mat(centList), clusterAssment

import urllib
import json
def geoGrab(stAddress, city):
    apiStem = 'http://where.yahooapis.com/geocode?'  #create a dict and constants for the goecoder
    params = {}
    params['flags'] = 'J'#JSON return type
    params['appid'] = 'aaa0VN6k'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = urllib.urlencode(params)
    yahooApi = apiStem + url_params      #print url_params
    print(yahooApi)
    c=urllib.urlopen(yahooApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(fileName):
    fw = open('places.txt', 'w')
    for line in open(fileName).readlines():
        line = line.strip()
        lineArr = line.split('\t')
        retDict = geoGrab(lineArr[1], lineArr[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print("%s\t%f\t%f" % (lineArr[0], lat, lng))
            fw.write('%s\t%f\t%f\n' % (line, lat, lng))
        else: print("error fetching")
        sleep(1)
    fw.close()
    
def distSLC(vecA, vecB):#Spherical Law of Cosines
    #print('vecA = ',vecA)
    #print('vecB = ',vecB)
    #print('vecA[0,1] = ',vecA[0,1])
    #print('sin(vecA[0,1]*pi/180) = ',sin(vecA[0,1]*pi/180))
    a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * \
                      cos(pi * (vecB[0,0]-vecA[0,0]) /180)
    return arccos(a + b)*6371.0 #pi is imported with numpy

import matplotlib
import matplotlib.pyplot as plt
def clusterClubs(numClust=5):
    datList = []
    for line in open('places.txt').readlines():
        lineArr = line.split('\t')
        datList.append([float(lineArr[4]), float(lineArr[3])])
    print('datList',datList)
    datMat = mat(datList)
    print('datMat',datMat)
    myCentroids, clustAssing = biKmeans(datMat, numClust, distMeas=distSLC)
    fig = plt.figure()
    rect=[0.1,0.1,0.8,0.8]
    scatterMarkers=['s', 'o', '^', '8', 'p', \
                    'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0=fig.add_axes(rect, label='ax0', **axprops)
    imgP = plt.imread('Portland.png')
    ax0.imshow(imgP)
    ax1=fig.add_axes(rect, label='ax1', frameon=False)
    for i in range(numClust):
        ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        print('markerStyle = ',markerStyle)
        ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()
