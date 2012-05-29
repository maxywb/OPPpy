"""****************************************************************************"""
# represents an item in a function
class FunctItem(object):

    def __init__(self,terminal,function, label):
        self.terminal = terminal
        self.function = function
        self.label = label
        self.group = None
        # __init__
# FunctItem

class FunctNode(object):
   
    def __init__(self, group):
        self.parentCtr = 0
        self.children = set() 
        self.group = set()  #set of items in the group this node represents
        self.group = group
    # __init__

    def printChildren(self):
        rep = "{ "
        for child in self.children:
            rep += str(child)+", "
        rep += " }"
        print rep
    # printChildren
# FunctNode
