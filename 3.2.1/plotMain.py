import treePlotter
import tree

myDat, labels = tree.createDataSet()
myTree = tree.createTree(myDat, labels)
print('myTree = ', myTree)
print('treePlotter.getNumLeafs(myTree) = ', treePlotter.getNumLeafs(myTree))
print('treePlotter.getTreeDepth(myTree) = ', treePlotter.getTreeDepth(myTree))
treePlotter.createPlot(myTree)
