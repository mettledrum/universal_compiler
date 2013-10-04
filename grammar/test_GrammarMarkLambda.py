# Andrew Hoyle

from GrammarAnalyzerClass import *

# runs ga methods, prints their final data member lists when made
def test(prods):
    ga = GrammarAnalyzerClass(prods)
    print "Productions:\t", ga.prodList
    print "\nLHS:\t\t", ga.LHS
    print "\nRHS:\t\t", ga.RHS
    print "\nSymbols:\t", ga.allSymbols
    print "\nTerminals:\t", ga.Terms
    print "\nnon-Terms:\t", ga.nonTerms
    print '\n'

    ga.markLambda()
    print "derivesLambda:\t", ga.derivesLambda

    ga.fillFirstSet()
    print "\nfirstSet:\t", ga.firstSet

# get file name with productions, run test with productions string
if __name__ == '__main__':
    #prFile = raw_input("type production file name: ")
    #f = open(prFile, 'r')
    f = open('MG1.txt', 'r')
    pr = f.read()
    test(pr)
