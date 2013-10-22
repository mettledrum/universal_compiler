# Andrew Hoyle

from GrammarAnalyzerClass import *

# runs ga methods, prints their final data member lists when made
# pass it the start file
def test(prods):
    ga = GrammarAnalyzerClass(prods)
    print "Productions:\t", ga.prodList
    print "\nLHS:\t\t", ga.LHS
    print "\nRHS:\t\t", ga.RHS
    print "\nSymbols:\t", ga.allSymbols
    print "\nTerminals:\t", ga.Terms
    print "\nnon-Terms:\t", ga.nonTerms

    ga.markLambda()
    print "\nderivesLambda:\t", ga.derivesLambda

    ga.fillFirstSet()
    print "\nfillSet:"
    for elem in ga.firstSet.iteritems():
        print elem
    
    # gotta pass method start symbol
    # NOTE: for customizing start symbol
    #st_sym = raw_input("\ntype start symbol: ")
    st_sym = "<systemGoal>"
    ga.fillFollowSet(st_sym)
    print "\nfollowSet:"
    for elem in ga.followSet.iteritems():
        print elem

    # run predict
    ga.fillPredictSet()
    print "\npredictSet:"
    for elem in ga.predictSet.iteritems():
        print elem
        
    # run tableGen, T(X,a)
    ga.tableGenerator()
    print "\ntable:"
    for elem in ga.predictTable.iteritems():
      print elem

    # test accessing an elem of tableGenerator
    #print ga.predictTable["<statement>"]["read"]

    # test the LLDriver
    #print "\ndriver:"
    #ga.LLDriver(st_sym)

# get file name with productions, run test with productions string
if __name__ == '__main__':
    # NOTE: for customizing grammar input
    #prFile = raw_input("type production file name: ")
    #f = open(prFile, 'r')
    f = open('MG1.txt', 'r')
    pr = f.read()
    test(pr)

