"""
parses the file that contains the definition of the grammar
"""
#definition = {"Add":"\+","Number":"[0-9]+(\.[0-9]+)?"}
#STRING_REP = "1:(* <); 2:(+ <)"

import os

class GrammarParser(object):
    
    gFile = None # the file that contains the definition of the grammar
    debug = False

    def __init__(self,gpath,debug=False):
        if not os.path.isfile(gpath):
            raise GParseFileError(gpath)
        self.gFile = open(gpath)
        self.debug=debug
    # __init__

    # returns the definiton of the tokens for the scanner and the relationships
    # between the terminal symbols for the parser
    def getDetails(self):
        definition = "{ "
        relations = ""
        hierarchy = list()
        # divvy up the file
        for line in iter(self.gFile):
            # check if the line is a comment or is blank
            if not line.strip():
                continue
            if line[0] == "#":
                continue
            # strip the meat out
            beginIndex = line.find("{")
            endIndex = line.find("}")
            meat = line[beginIndex+1:endIndex]
            meat = meat.strip()
            # deal with the different tokens for the scanner
            for token in meat.split(";"):
                parts = token.split(",")
                name = parts[0]
                regex = parts[2]
                # format the name and regex to fit what the scanner expects
                definition += "("+name+":"+regex+");"
            # deal with the relations
            index = int(line.split(":")[0])
            hierarchy.insert(index,meat)
            
        # add the terminator for the scanner's token string
        definition += "}"

        # make the parser relations

        levelCtr = 1        
        for level in hierarchy:
            details = ""
            for items in level.split(";"):
                parts = items.split(",")
                name = parts[0]
                assoc = parts[1]
                details+= "("+name+":"+assoc+"),"
            relations += str(levelCtr)+":"+details[0:len(details)-1]+";"
            levelCtr +=1
        # remove empty, final relation
        relations= relations[0:len(relations)-1]
        if(self.debug): 
            print "definition:"
            print definition
            print "relations:"
            print relations

        return definition,relations
# getDetails



class GParseFileError(Exception):
    def __init__(self,path):
        self.path = path
    def __str__(self):
        return "Path to grammar file is bad: "+self.path
# GParseFileError
