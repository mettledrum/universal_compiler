# Andrew Hoyle

from GrammarAnalyzerClass import *

# runs ga methods, prints their final data member lists when made
# pass it the start file
def test(prods):
    ga = GrammarAnalyzerClass(prods)

    # runs everything to get all the sets populated
    ga.populateSets()

    print "Productions:\t", ga.prodList
    print "\nLHS:\t\t", ga.LHS
    print "\nRHS:\t\t", ga.RHS
    print "\nSymbols:\t", ga.allSymbols
    print "\nTerminals:\t", ga.Terms
    print "\nnon-Terms:\t", ga.nonTerms

    print "\nderivesLambda:\t", ga.derivesLambda

    print "\nfillSet:"
    for elem in ga.firstSet.iteritems():
        print elem
    
    print "\nfollowSet:"
    for elem in ga.followSet.iteritems():
        print elem

    print "\npredictSet:"
    for elem in ga.predictSet.iteritems():
        print elem

    print "\ntableGenerator"
    for elem in ga.predictTable.iteritems():
        print elem

# get file name with productions, run test with productions string
if __name__ == '__main__':
    # NOTE: for customizing grammar input
    #prFile = raw_input("type production file name: ")
    #f = open(prFile, 'r')
    f = open('MG1.txt', 'r')
    pr = f.read()
    test(pr)

