import bayes
from numpy import *
listOposts, listClasses = bayes.loadDataSet()
myVocabList = bayes.createVocabList(listOposts)
trainMat = []
print("-----start for about trainMat----- ")
for postinDoc in listOposts: 
    print("postinDoc = ", postinDoc)
    trainMat.append(bayes.setOfWords2Vec(myVocabList, postinDoc))
    print("trainMat = ", trainMat)

p0V, p1V, pAb = bayes.trainNB0(trainMat, listClasses)
print("p0V = ", p0V)
print("p1V = ", p1V)
print("pAb = ", pAb)
