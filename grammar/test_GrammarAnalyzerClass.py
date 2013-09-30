# Andrew Hoyle

from GrammarAnalyzerClass import *

def test(prods):
    ga = GrammarAnalyzerClass(prods)
    print "Productions:\t", ga.prodList
    print "LHS:\t\t", ga.LHSList
    print "RHS:\t\t", ga.RHSList
    print "Symbols:\t", ga.allSymbols
    print "Terminals:\t", ga.Terms
    print "non-Terms:\t", ga.nonTerms

# get file name with productions, run test with productions string
if __name__ == '__main__':
    prFile = raw_input("type production file name: ")
    f = open(prFile, 'r')
    #f = open('MicroGrammar2.txt', 'r')
    pr = f.read()
    test(pr)
