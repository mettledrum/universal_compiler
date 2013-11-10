# Andrew Hoyle

from GrammarAnalyzerClass import *

def test(prods):
    ga = GrammarAnalyzerClass(prods)
    print "\nProductions:\t", ga.prodList
    print "\nLHS:\t\t", ga.LHS
    print "\nRHS:\t\t", ga.RHS
    print "\nRHS with actions:\t", ga.RHS_with_actions
    print "\nSymbols (no actions):\t", ga.allSymbols
    print "\nTerminals:\t", ga.Terms
    print "\nnon-Terms:\t", ga.nonTerms
    print '\n'

# get file name with productions, run test with productions string
if __name__ == '__main__':
    #prFile = raw_input("type production file name: ")
    #f = open(prFile, 'r')
    f = open('MG1_with_actions.txt', 'r')
    pr = f.read()
    test(pr)
