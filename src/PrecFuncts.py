"""****************************************************************************"""
from Util import *
from PrecUtil import *
class PrecFuncts(object):
    LEFT_ASSOC = "<"
    RIGHT_ASSOC = ">"
    NEITHER_ASSOC = "-"
    
    def __init__(self,stringRep,debug):
        self.debug = debug
        self.f = dict()
        self.g = dict()
        self.lens = dict()
        rels = Relations(stringRep,debug)
        if self.debug : relations.printState()
        keys, hierarchy = self.parseRelations(stringRep)
        self.makePrecedenceFuncts(self.f,self.g,self.lens,keys,hierarchy,rels)
    # __init__
    
    def getFuncts(self):
        return self.f,self.g
    # getFuncts

    def makePrecedenceFuncts(self,f,g,lens,keys,hierarchy,relations):
        if self.debug:print "making precedence functions:"

        items = list()
        for level in hierarchy:
            for key in level:
                # create symbols for each terminal symbol
                f[key] = None
                g[key] = None
                items.append(FunctItem(key,f,"f("+key+")"))
                items.append(FunctItem(key,g, "g("+key+")"))
        
        # sort the items into their groups
        groups = set()
        for item in items:
            # base case
            if len(groups) == 0:
                curGroup = set()
                curGroup.add(item)
                groups.add(frozenset(curGroup))
            # find the appropriate group
            found = False
            foundGroup = None                
            for curGroup in groups:
                for other in curGroup:
                    if relations.areEqual(item.terminal,other.terminal):
                        functA = "f"
                        functB = "f"
                        if item.function is not f: functA = "g"
                        if other.function is not f: functB = "g"
                        if self.debug:print functA+"(",item.terminal+")",".=",functB+"(",other.terminal+")"
                        foundGroup = curGroup
                        found = True
                        break
                if found:
                    break
            if found:
                groups.remove(foundGroup)
                newSet = set(foundGroup)
                newSet.add(item)
                groups.add(frozenset(newSet))
            # if there is no group, add one
            else:
                curGroup = set()
                curGroup.add(item)
                groups.add(frozenset(curGroup))

        # make the graph

        nodes = self.makeDAG(f,g,groups,relations,items)
        
        if self.debug:
            for node in nodes:
                print "node:",id(node)
                rep = "{"
                for item in node.group:
                    funct = "g"
                    if item.function is f:
                        funct = "f"
                    rep += ","+funct+"("+item.terminal+")"
                rep +="}"
                print "group:",rep
                rep = "{"
                for child in node.children:
                    rep+=","+str(id(child))
                rep += "}"
                print "children:",rep
                print ""

        # check for cycles
        self.findCycles(nodes)

        # define f and g
        self.mapLengths(f,g,nodes)

    # makePrecedenceFuncts

    def makeDAG(self,f,g,groups,relations,items):
        
        # make a node for each group
        nodes = list()
        for curGroup in groups:
            nodes.append(FunctNode(curGroup))

        # make graph
        for fa in f:
            nodeA = self.findNode(fa,f,nodes)
            for gb in g:
                nodeB = self.findNode(gb,g,nodes)
                if relations.yieldsTo(fa,gb):
                    if self.debug:print "f("+fa+")","(",id(nodeA),") <.","g("+gb+")","(",id(nodeB),")"
                    nodeB.children.add(nodeA)
                    nodeA.parentCtr += 1
                elif relations.yieldsTo(gb,fa):
                    if self.debug:print "f("+fa+")","(",id(nodeA),") .>","g("+gb+")","(",id(nodeB),")"
                    nodeA.children.add(nodeB)
                    nodeB.parentCtr += 1

                
        return nodes
    # makeDAG

    def findCycles(self,nodes):
        S = set()
        for node in nodes:
            if node.parentCtr == 0:
                S.add(node)
        while len(S) > 0:
            node = S.pop()
            for child in node.children:
                child.parentCtr -= 1
                if child.parentCtr == 0:
                    S.add(child)
        if len(S) > 0:
            raise ParseError("cycle detected")
                
        return False
    # findCycles

    def findNode(self,terminal,function,nodes):
        for node in nodes:
            for item in node.group:
                if item.terminal == terminal and item.function is function:
                    return node
        return None
    # findNode

    def yields(self, a, b):
        ctr = len(self.hierarchy)
        levelA = -1
        levelB = -1
        for level in self.hierarchy:
            if a in level:
                levelA = ctr
            if b in level:
                levelB = ctr
            ctr -= 1
        if levelA < levelB:
            return True
        else:
            return False
    # yields
        
    def mapLengths(self,f,g,nodes):
        # initialize the lengths
        lenTo = dict()
        for node in nodes:
            lenTo[node]=0
            
        # calculate the lengths
        for node in nodes:
            for child in node.children:
                lenTo[child]=lenTo[node]-1
        
        # set the lengths in the f and g functions

        seen = set()
        for node in nodes:
            for item in node.group:
                key = item.terminal
                function = item.function
                function[key] = lenTo[node]
            seen.add(node)
        if self.debug:
            for fa in f:
                print "f("+fa+") =",f[fa]
            for gb in g:
                print "g("+gb+") =",g[gb]

    # mapLengths
                   
    def findLeaves(self,nodes):
        leaves= list()
        seen = set()
        for node in nodes:
            runner = node
            stack = Stack() # only need to visit each node once
            stack.push(runner)
            while runner:
                
                # don't re-visit nodes from previous passes
                if runner in seen:
                    runner = stack.pop()
                    continue
                # if the node is a leaf, add it to leaves
                if len(runner.children) == 0:
                    leaves.append(runner)
                else:
                    for next in runner.children:
                        stack.push(next)
                runner = stack.pop()
                seen.add(runner)
        return leaves
    # findLeaves
    
    def findRoot(self, nodes):
        largest = 1
        root = None
        for node in nodes:
            runner = node
            height = 1
            while runner:
                height+=1
                runner = runner.parent
            if height > largest:
                largest = height
                root = node
        return runner
    # findRoot

    def parseRelations(self,relations):
        levels = relations.split(";")
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
        # make the map of terminals to terms they are equal with
        keys = list()
        for level in hierarchy:
            for term in level:
                keys.append(term)

        return keys, hierarchy
    # parseRelations
# PrecedenceFunct
