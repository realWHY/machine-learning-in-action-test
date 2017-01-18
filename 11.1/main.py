import apriori

dataSet = apriori.loadDataSet()
L, suppData = apriori.apriori(dataSet)
rules = apriori.generateRules(L,suppData,minConf=0.5)
