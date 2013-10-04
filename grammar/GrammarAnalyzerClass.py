# Andrew Hoyle

import string                               # parsing strings
from collections import defaultdict         # "multidict' functionality

# breaks up predicate rules into pieces
# pr MUST be formatted with \n between rules, and ONE ' ' between symbols
class GrammarAnalyzerClass:
    # constructor, takes pr, generates data member lists
    # takes string representing productions
    def __init__(self, pr):
        # break up by '\n'
        self.prodList = string.split(pr, '\n')
        # get rid of ''(s) from last line(s)
        while '' in self.prodList:
            self.prodList.remove('')

        # put values into LHS[], RHS[[]], and allSymbols[] 
        self.LHS = []
        self.RHS = []
        self.allSymbols = []
        self.getSymbols()

        # look for '<' in elements
        self.Terms = []
        self.nonTerms = []
        self.getNT()

        # remove duplicates
        self.removeDups()

        # key ['symbol_name'] = True/False
        self.derivesLambda = dict()

        # productions counter
        self.prodCount = len(self.prodList)

        # keys = {...}
        self.firstSet = defaultdict(set)
        self.followSet = defaultdict(set)

    # remove duplicates of lists using set functions
    # helps constructor
    # NOTE: not sure if 'lambda' should be in certain lists
    def removeDups(self):
        self.allSymbols = set(self.allSymbols)
        #self.allSymbols.discard('lambda')
        self.allSymbols = list(self.allSymbols)

        self.Terms = set(self.Terms)
        #self.Terms.discard('lambda')
        self.Terms = list(self.Terms)

        self.nonTerms = set(self.nonTerms)
        #self.nonTerms.discard('lambda')
        self.nonTerms = list(self.nonTerms)

    # takes list of productions, breaks up by ' '
    # puts in RHS and LHS lists
    # helps constructor
    def getSymbols(self):
        for p in self.prodList:
            _symbols = string.split(p, ' ')
            # put first symbol into LHS and allSymbols
            self.LHS.append(_symbols[0])
            self.allSymbols.append(_symbols[0])

            # put list of symbols into RHS
            self.RHS.append(_symbols[2:])

            for s in _symbols[2:]:
                self.allSymbols.append(s)

    # looks for '<' in elems' first place, means its a non-term
    # helps constructor
    def getNT(self):
        for s in self.allSymbols:
            if s[0] == '<':
                self.nonTerms.append(s)
            else:
                self.Terms.append(s)

    '''----------------------------------------------------------------------'''
    
    # populates self.derivesLambda
    # NOTE: looks ahead multiple times or just ONCE? are notes wrong?
    def markLambda(self):
        # local vars for while loop
        _changes = True
        _RHS_DerivesLambda = bool
    
        # initialize derivesLambda data members all to False
        # NOTE: make 'lambda' True because and operation
        for v in self.allSymbols:
            self.derivesLambda[v] = False
        self.derivesLambda['lambda'] = True     # NOTE: needed?

        # make changes to derivesLambda using RHS
        while _changes:
            # determines when to exit while loop
            _changes = False
            # iterate through each production
            for p in range(self.prodCount):
                _RHS_DL = True
                # if lambda isn't inside RHS(p)
                if True:     # NOTE: |{lambda}| = 0, self.RHS[p] != ['lambda']
                    # iterate through each elem of RHS(p)
                    for i in range(len(self.RHS[p])):
                        # for each symbol in the RHS of prod p
                        _RHS_DL = _RHS_DL and self.derivesLambda[self.RHS[p][i]]
                    # if change made, go again through while loop
                    if _RHS_DL and not self.derivesLambda[self.LHS[p]]:
                        _changes = True
                        # make LHS True
                        self.derivesLambda[self.LHS[p]] = True

    # called by FillFirstSet() method
    # returns a set
    # NOTE: indexing in notes is [1 n], here it's [0 n-1]
    def computeFirst(self, x):
        # local vars
        _result = set()
        k = len(x)
        # go through each element of x
        if k == 0:      # NOTE: maybe the 0 here was to ignore lambda
            _result.add('lambda')
        else:
            # union firstSet's values to it
            _result |= self.firstSet[x[0]]
            _result.discard('lambda')

        # start index
        i = 0   # NOTE: index starts at 0 or 1?
        while i < (k-1) and 'lambda' in self.firstSet[x[i]]:
            i += 1
            # take out lambda if it's inside
            _result |= self.firstSet[x[i]]
            _result.discard('lambda')
        # last elem of x
        if i == (k-1) and 'lambda' in self.firstSet[x[k-1]]:
            _result.add('lambda')

        return _result

    # utility for fillFirstSet()
    # takes non-term and term respectively
    # matches LHS[i]==A and RHS[i][0] == a
    def A_a(self, A, a):
        for i in range(self.prodCount):
            if self.LHS[i] == A and self.RHS[i][0] == a:
                return True
        return False

    # populates first set for all symbols
    def fillFirstSet(self):
        # init firstSet for nonTerms
        for A in self.nonTerms:
            if self.derivesLambda[A]:
                self.firstSet[A].add('lambda')

        # NOTE: debugging print statement
        #print "loop 1 firstSet:\t", self.firstSet
        
        # init firstSet for Terms
        for a in self.Terms:
            self.firstSet[a].add(a)
            for A in self.nonTerms:
                # A -> a... match found in p
                if self.A_a(A, a):
                    self.firstSet[A].add(a)
                    # NOTE: debugging print statement
                    #print "match found:\t", A, "->", a

        # NOTE: debugging print statement
        #print "loop 2 firstSet:\t", self.firstSet

        # NOTE: lambda was getting stripped off because of Python's pointers...
        #  When I made sets = local set... It wasn't by value, so the
        #  self.firstSets was being changed too

        # add to firstSet
        _changes = 0        # NOTE: need to sense changes better
        while _changes < 20:
            _changes += 1   # NOTE: need to sense changes better
            for p in range(self.prodCount):
                self.firstSet[self.LHS[p]] |= self.computeFirst(self.RHS[p])



                
                



        

