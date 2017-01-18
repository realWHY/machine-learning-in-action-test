'''
Created on Mar 24, 2011
Ch 11 code
@author: Peter
'''
from numpy import *
from pdb import set_trace as bp
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            #print("[item]", [item])    
            if not [item] in C1:
                C1.append([item])
    #print("C1 before sort", C1)            
    C1.sort()
    #print("C1 after sort", C1)
    return list(map(frozenset, C1))#use frozen set so we
                            #can use it as a key in a dict    

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    print("ssCnt = ",ssCnt)
    numItems = float(len(D))
    print("numItems = ",numItems)
    retList = []
    supportData = {}
    for key in ssCnt:
        print("key = ",key)
        print("ssCnt[key] = ",ssCnt[key])
        support = ssCnt[key]/numItems
        print("support = ",support)
        if support >= minSupport:
            retList.insert(0,key)
            print("retList = ",retList)
        supportData[key] = support
    print("supportData = ",supportData)
    print("retList = ",retList)
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    print("Lk=",Lk)
    print("k=",k)
    print("lenLk=",lenLk)
    for i in range(lenLk):
        print("i=",i)
        for j in range(i+1, lenLk):
            print("j=",j)
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            print("L1 = ",L1)
            print("L2 = ",L2)
            L1.sort(); L2.sort()
            print("L1 after sort= ",L1)
            print("L2 after sort= ",L2)
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
            print(Lk[i] | Lk[j])
            print("retList",retList)
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    print("L = ",L)
    k = 2
    while (len(L[k-2]) > 0):
        print("L in while= ",L)
        Ck = aprioriGen(L[k-2], k)
        #bp()
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    print("----------------------------------")
    print("len(L)",len(L))
    print("L",L)
    print("supportData",supportData)
    print("minConf",minConf)
    print("----------------------------------")
    for i in range(1, len(L)):#only get the sets with two or more items
        print("i",i)
        for freqSet in L[i]:
            print("freqSet",freqSet)
            H1 = [frozenset([item]) for item in freqSet]
            print("H1 = ",H1)
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
        bp()
    return bigRuleList         

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = [] #create new list to return
    for conseq in H:
        print("conseq = ",conseq)
        print("freqSet = ",freqSet)
        print("freqSet-conseq = ",freqSet-conseq)
        print("supportData[freqSet-conseq] = ",supportData[freqSet-conseq])
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf: 
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            print("brl = ",brl)
            prunedH.append(conseq)
            print("prunedH = ",prunedH)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    print("m = ",m)
    print("len(freqSet) = ",len(freqSet))
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            
def pntRules(ruleList, itemMeaning):
    for ruleTup in ruleList:
        for item in ruleTup[0]:
            print(itemMeaning[item])
        print("           -------->")
        for item in ruleTup[1]:
            print(itemMeaning[item])
        print("confidence: %f" % ruleTup[2])
        print()       #print a blank line
        
'''           
from time import sleep
from votesmart import votesmart
votesmart.apikey = 'get your api key first'
def getActionIds():
    actionIdList = []; billTitleList = []
    fr = open('recent20bills.txt') 
    for line in fr.readlines():
        billNum = int(line.split('\t')[0])
        try:
            billDetail = votesmart.votes.getBill(billNum) #api call
            for action in billDetail.actions:
                if action.level == 'House' and \
                (action.stage == 'Passage' or action.stage == 'Amendment Vote'):
                    actionId = int(action.actionId)
                    print('bill: %d has actionId: %d' % (billNum, actionId))
                    actionIdList.append(actionId)
                    billTitleList.append(line.strip().split('\t')[1])
        except:
            print("problem getting bill %d" % billNum)
        sleep(1)                                      #delay to be polite
    return actionIdList, billTitleList
'''       
def getTransList(actionIdList, billTitleList): #this will return a list of lists containing ints
    itemMeaning = ['Republican', 'Democratic']#list of what each item stands for
    for billTitle in billTitleList:#fill up itemMeaning list
        itemMeaning.append('%s -- Nay' % billTitle)
        itemMeaning.append('%s -- Yea' % billTitle)
    transDict = {}#list of items in each transaction (politician) 
    voteCount = 2
    for actionId in actionIdList:
        sleep(3)
        print('getting votes for actionId: %d' % actionId)
        try:
            voteList = votesmart.votes.getBillActionVotes(actionId)
            for vote in voteList:
                if not transDict.has_key(vote.candidateName): 
                    transDict[vote.candidateName] = []
                    if vote.officeParties == 'Democratic':
                        transDict[vote.candidateName].append(1)
                    elif vote.officeParties == 'Republican':
                        transDict[vote.candidateName].append(0)
                if vote.action == 'Nay':
                    transDict[vote.candidateName].append(voteCount)
                elif vote.action == 'Yea':
                    transDict[vote.candidateName].append(voteCount + 1)
        except: 
            print("problem getting actionId: %d" % actionId)
        voteCount += 2
    return transDict, itemMeaning
