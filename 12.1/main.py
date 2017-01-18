import fpGrowth

rootNode = fpGrowth.treeNode('pyramid',9, None)
rootNode.children['phoenix'] = fpGrowth.treeNode('phoenix',3,None)
rootNode.disp()
