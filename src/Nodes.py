"""
Important stand-alone nodes
"""

""" Node should never be instantiated """
class Node(object):
    def __init__(self):
        self.value = None
        self.type = None
    # __init__

    """ print a simple representation of the Node """
    def toString(self):
        rep = str(self.type) + ": " + str(self.value)
        return rep
    # toString

    def equals(self, other):
        #equals method is funky becuase dynamic classes are weird
        try:
            if not self.value == other.value:
                return False
            if not self.type == other.type:
                return False
            return True
        except:
            return False
    # equals
# Node

class Error(Node):
    def toString(self):
        rep = str(self.type) + ": \n"
        rep += str(self.value) + "\n"
        rep +="^ is bad \n"
        return rep
    # toString
# Error

class EOF(Node):
    def toString(self):
        rep = "End of File: "+self.value
        return rep
    # toString
# EOF
