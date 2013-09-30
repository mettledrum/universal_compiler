# Andrew Hoyle

import string

# breaks up predicate rules into pieces
# pr MUST be formatted with \n between rules, and ONE ' ' between symbols
class GrammarAnalyzerClass:
    # constructor, takes pr, generates data member lists
    def __init__(self, pr):
        # break up by '\n'
        self.prodList = string.split(pr, '\n')
        # get rid of ''(s) from last line(s)
        while '' in self.prodList:
            self.prodList.remove('')

        # put values into LHS RHS
        self.LHSList = []
        self.RHSList = []
        self.getSymbols()

        self.allSymbols = self.LHSList + self.RHSList

        # look for '<' in elements
        self.Terms = []
        self.nonTerms = []
        self.getNT()

        # remove duplicates
        self.removeDups()

    # remove duplicates of lists using set functions
    def removeDups(self):
        self.LHSList = list(set(self.LHSList))
        self.RHSList = list(set(self.RHSList))
        self.allSymbols = list(set(self.allSymbols))
        self.Terms = list(set(self.Terms))
        self.nonTerms = list(set(self.nonTerms))

    # takes list of productions, breaks up by ' ' 
    def getSymbols(self):
        for p in self.prodList:
            _symbols = string.split(p, ' ')
            self.LHSList.append(_symbols[0])

            for s in _symbols[2:]:
                self.RHSList.append(s)

    # looks for '<' in elems' first place, means its a non-term
    def getNT(self):
        for s in self.allSymbols:
            if s[0] == '<':
                self.nonTerms.append(s)
            else:
                self.Terms.append(s)


