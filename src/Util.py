"""****************************************************************************"""
"""
utility classes for the Parser class
"""


""" 
represents the ralationshipbetween different terminal symbols. assumes that the grammar 
contains numbers and that numbers dominate all
"""
class Relations(object):
    LEFT_ASSOC = "<"
    RIGHT_ASSOC = ">"
    NEITHER_ASSOC = "-"
    hierarchy = None # hierarchy of terminals ymbols
    terminals_ = None # list of all terminal symbols
    associativity = None # maps terminals to their associativity
    yields = None # map of terminals to the terminals it yields to
    dominates = None # map of terminals to the terminals it dominates
    equal = None # map of terminals to the terminals with the same precedence

    def __init__(self, stringRep, debug):
        self.debug = debug
        self.hierarchy, self.terminals, self.associativity = self.makeHierarchy(stringRep)
        self.yields = self.makeYields(self.hierarchy, self.associativity, self.terminals)
        self.dominates = self.makeDominates(self.hierarchy, self.terminals)
        self.equal = self.makeEqual(self.hierarchy)
        if self.debug: self.printState()
    # __init__

    def printState(self):
        print "yields:\n",self.yields
        print "dominates:\n",self.dominates
        print "equal:\n",self.equal
    # printState

    def makeDominates(self, hierarchy, terminals):
        hierCtr = len(hierarchy)-1
        dominates = dict()

        # setup the map
        for term in terminals:
            dominates[term]=set()
        
        least = list() # the low level terminals already seen

        while hierCtr >= 0:
            # ensure that all terminals yield to those of a higher level
            curLevel = hierarchy[hierCtr]
            for term in curLevel:
                domSet = dominates.get(term)
                for lower in least:
                    domSet.add(lower)

            # add the terminals already seen to the least list
            least += curLevel
            hierCtr-=1

        return dominates
    # makeDominates

    def getSameAssoc(self, level, assoc):
        same = list()
        for term in self.hierarchy[level]:
            if self.associativity[term] == assoc:
                same.append(term)
        return same
    # getLeftAssoc

    def makeYields(self, hierarchy, associativity, terminals):
        hierCtr = 0
        yields = dict()

        # setup the map
        for term in terminals:
            yields[term]=set()
        
        greats = list() # the high level terminals already seen

        # make all the yield relations
        while hierCtr < len(self.hierarchy):

            left = self.getSameAssoc(hierCtr, self.LEFT_ASSOC)
            right = self.getSameAssoc(hierCtr, self.RIGHT_ASSOC)
            neither = self.getSameAssoc(hierCtr, self.NEITHER_ASSOC)
            
            # make the relatins between left associative terms and others
            for term in left:
                yieldSet = yields.get(term)
                # left associative yields to left associative (including itself)
                for otherTerm in left:
                    yieldSet.add(otherTerm)
                # left associative yields to right associative
                for otherTerm in right:
                    yieldSet.add(otherTerm)
                # non associative terms yield to left associative terms
                for otherTerm in neither:
                    yieldSet = yields.get(otherTerm)
                    yieldSet.add(term)
                
            # make the relations between right associative terms and others
            for term in right:
                yieldSet = yields.get(term)
                # right associative yields to right associative
                for otherTerm in right:
                    yieldSet.add(otherTerm)
                # non associative terms yield to right associative terms
                for otherTerm in neither:
                    yieldSet = yields.get(otherTerm)
                    yieldSet.add(term)
            # non associative terms should never come back-to-back, this is an error

            # ensure that all terminals yield to those of a higher level
            curLevel = hierarchy[hierCtr]
            for term in curLevel:
                yieldSet = yields.get(term)
                for greater in greats:
                    yieldSet.add(greater)

            # add the terminals already seen to the greats list
            greats += curLevel
            hierCtr+=1

        return yields
    # makeYields

    def makeEqual(self,hierarchy):
        equal = dict()
        for level in hierarchy:
            for term in level:
                samePrec = set(level)
                samePrec.remove(term)
                equal[term]=samePrec
        # if any item in set dominates or yields to any other it should be removed
        remove = set()
        for item in equal:
            for other in equal:
                if self.yieldsTo(item,other) or self.dominate(item,other):
                    remove.add(item)
        for rem in remove:
            equal.pop(rem)
        return equal
    # makeEqual

    def makeHierarchy(self, rep):
        levels = rep.split(";")
        hierarchy = list()
        associativity = dict()
        hierCtr = 0
        terminals = set()
        for level in levels:
            curLevel = set()
            startIndex = level.find(":")
            curTerms = level[startIndex+1:len(level)]
            for terminal in curTerms.split(","):
                # formate the input as nicely as possible
                definition = terminal.split("(")[1]
                definition = definition.split(")")[0]
                # extract the term and associativity
                parts = definition.split(":")
                term = parts[0].strip()
                assoc = parts[1].strip()
                if not assoc == self.LEFT_ASSOC and not assoc == self.RIGHT_ASSOC \
                        and not assoc == self.NEITHER_ASSOC:
                    raise ParseError("Bad associativity symbol : "+assoc)
                associativity[term]=assoc
                curLevel.add(term)
                terminals.add(term)
            hierarchy.insert(hierCtr,curLevel)
            hierCtr+=1            
        return hierarchy, terminals, associativity
    # makeHierarchy
  
    # returns the set of terminals that are equal to item
    def getEqual(self, item):
        return self.equal.get(item)
    # getEqual

    # return True if item and other have the same precedence
    def areEqual(self,item, other):
        sames = self.equal.get(item)
        if sames:
            return other in sames
        return False
    # areEqual

    # returns True if item dominates other
    def dominate(self,item, other):
        doms = self.dominates.get(item)
        if doms:
            return other in doms
        return False
    # dominates

    # returns True if item yields to other
    def yieldsTo(self,item, other):
        yields = self.yields.get(item)
        if yields:
            return other in yields
        return False
    # yields
# Relations

class ParseError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
# ParseError
        
class Stack(object):

    def __init__(self):
        self.stack = list()
        self.sp = 0
    # __init__
    def peek(self):
        return self.sp > 0
    # peek

    def top(self):
        if self.peek():
            return self.stack[self.sp-1]
        else:
            return None
    # top

    def pop(self):

        if self.peek():
            self.sp -= 1
            item = self.stack[self.sp]
            return item
        else:
            return None
    # pop
    
    def push(self, item):
        self.sp += 1
        self.stack.insert(self.sp-1,item)
    # push

    def pushAll(self, items):
        for item in items:
            self.push(item)
    # pushAll
# Stack

