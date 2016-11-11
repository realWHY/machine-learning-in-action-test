import tree
import treePlotter
fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
print('lenses= ',lenses)
lensesLabels=['age','prescript','astigmatic','tearrate']
lensesTree  = tree.createTree(lenses,lensesLabels)
print('lensesTree= ',lensesTree)
treePlotter.createPlot(lensesTree)
 
