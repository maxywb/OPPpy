from Nodes import *
import re
import new

#MAIN
if __name__ == "__main__":
    tokens = makeTokens()
    keyList, lexemes = makeLexemes(tokens)
    classes, classNames = makeClassTypes(keyList)
    functs = makeDeclFuncts(keyList, classNames, classes)
    scanner = makeScanner(lexemes,keyList,functs)

    print "testing: "
    tokens, remainder = scanner.scan("1+2+3?")
    
    print "tokens: "
    for t in tokens:
        print t.toString()

#MAIN
