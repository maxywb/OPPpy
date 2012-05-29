import re
import new
import __builtin__
from Nodes import *

class Scanner(object):
    
    def __init__(self, offset, phrase, definition, debug=False):

        self.debug = debug
        self.definition = definition
        self.phrase = phrase

        self.tokens = self.formatTokens(self.definition)
        self.keyList, self.lexemes = self.makeLexemes(self.tokens)
        self.classes, self.classNames = self.makeClassTypes(self.keyList)
        self.updateBuiltins(self.lexemes,self.keyList,self.classes, self.classNames)
        self.functs = self.makeDeclFuncts(self.keyList, self.classNames, self.classes)
        self.scanner = self.makeScanner(self.lexemes,self.keyList,self.functs, self.classes)

        if self.debug:
            self.printState()
    # __init__

    """ returns all the information needed to parse the output of this class"""
    def getParseInfo(self):
        return self.classes, self.lexemes, self.keyList, self.tokens
    # getParseInfo

    def printState(self):
        print "Scanner"
        print "phrase:"
        print self.phrase
        print "definition:"
        print self.definition
        print "lexemes:"
        print self.lexemes
        print "keys:"
        print self.keyList
        print "functs:"
        print self.functs
    # printState

    def updateBuiltins(self, lexemes, keyList, classes, classNames):
        # ensure that Error is last so that when the scanner is created, ".*" won't match
        # anything it isn't supposed to
#        keyList.insert(len(keyList),"EOF")
        keyList.insert(len(keyList),"Error")
 
#        classes["EOF"]=EOF
        classes["Error"]=Error

#        classNames["EOF"]="EOF"
        classNames["Error"]="Error"
    
#        lexemes["EOF"]="\$"
        lexemes["Error"]=".*"
    # updateBuiltins

    def makeLexemes(self, tokens):
        keys = list()
        lexemes = dict()
        for key in tokens.keys():
            regex = tokens.get(key)
            lexemes[key] = regex
            keys.append(key)
        return keys, lexemes         
    # makeLexemes

    def stripToken(self, token):
        # find the opening (
        startIndex = token.find("(")
        if startIndex < 0: startIndex = 0
        #find the closing )
        end = len(token)
        tmpIndex = token.find(")",0,end)
        endIndex = -1
        begin = startIndex
        while tmpIndex > 0:
            endIndex = tmpIndex
            tmpIndex = token.find(")",begin,end)
            begin = tmpIndex + 1

        return token[startIndex+1:endIndex].strip()
    # stripToken

    def formatTokens(self, definition):
        tokens = dict()
        for tokenDef in definition.split(";"):
            meat = self.stripToken(tokenDef)
            parts = meat.split(":")
            if len(parts) > 1:
                name = parts[0].strip()
                regex = parts[1].strip()
                tokens[name] = regex
        return tokens
    # formatTokens

    def makeClass(self, name):
        cl = type(
            name,
            (Node,),
            dict(
                value = None,
                type = name,
                )
            )
        return cl
    # makeClass

    def makeClassTypes(self, keyList):
        classes = dict()
        classNames = dict()    
        for key in keyList:
            classType = self.makeClass(key)
            className = key
            classes[key]=classType
            classNames[key]=className
            setattr(__builtin__, className, classType)
        
        return classes, classNames
    # makeClassTypes

    def makeDeclFuncts(self, keyList,classNames,classes):
        functs = dict()
        for key in keyList:

            className = classNames.get(key)
            functName = className+"Const"

            functStr = "\
def "+functName+"(scanner,token):\
node= "+className+"(); node.type = \""+className+"\"; node.value = token; return node"
            functCo = compile(functStr,'','exec')
            ns = {}
            exec functCo in ns
            funct = new.function(ns[functName].func_code,globals(),functName)
            globals()[functName]=funct
            functs[key]=functName

        return functs
    # makeDeclFuncts

    def makeScanner(self, lexemes, keyList, functs, classes):
        self.lexItems = []
        keyCtr = 0
        while keyCtr < len(keyList):
            key = keyList[keyCtr]
            keyCtr+=1
            regex = lexemes.get(key)
            nodeType = classes.get(key)
            self.lexItems+=([(regex,globals()[functs.get(key)])])
        scanner = re.Scanner(self.lexItems)

        return scanner
    # makeScanner


    def scan(self):
        self.tokens, self.remainder = self.scanner.scan(self.phrase)
        
        if self.debug:
            print "tokens: "
            for t in self.tokens:
                print t.toString()
    # scan

# Scanner










