# Andrew Hoyle

# get class modules from sub-directories
from grammar.GrammarAnalyzerClass import GrammarAnalyzerClass
from scanner.ScannerClass import ScannerClass
from CompilerClass import CompilerClass

# instantiates scanner, ga,
# passes CLEANED scanner list to instantiated compiler
def test(prods, user_code_lines):
    # instantiate ga
    ga = GrammarAnalyzerClass(prods)
    # populate the set data members for generator
    # NOTE: start_symbol default used here
    ga.populateSets()

    # print debugging
    print "nonTerms:\t", ga.nonTerms
    print "\nTerms:\t", ga.Terms

    # instantiate scanner
    sc = ScannerClass(user_code_lines)
    # list to hold the output for error checking
    scan_out = []
    # run UNTIL EOF symbol found
    # NOTE: returns triple of info about token passed
    # NOTE: EOF hard-coded here
    while sc.code[0] != '$':
        scan_out.append(sc.Scanner())

    # NOTE: cleans scanner list of undesirable tokens
    scan_out_clean = cleaner(scan_out)
    print "\nScanner:\t", scan_out_clean, '\n'

    # give CLEANED scanner list to compiler object
    comp = CompilerClass(scan_out_clean, ga, 'compiler_output.txt')

    # NOTE: debugging print
    print "Productions:\t", ga.prodList
    print "\nLHS:\t\t", ga.LHS
    print "\nRHS:\t\t", ga.RHS
    print "\nAll Symbols:\t", ga.allSymbols
    print "\nTerminals:\t", ga.Terms
    print "\nnon-Terms:\t", ga.nonTerms
    print "\nActions:\t", ga.actions


    # NOTE: debugging print
    print "\npredict table: "
    for elem in ga.predictTable.iteritems():
        print elem
    print "\n"

    # run the driver
    comp.LLCompiler()

    # show variable name table
    print comp.var_table

# cleans that list of junk using token names from scanner
# this should be a scanner function maybe
# gets rid of 'EmptySpace' and 'Comment'
def cleaner(token_list):
    # do it a lot
    for c in range(0,len(token_list)):
        for el in token_list:
            if el[2] == 'Comment':
                token_list.remove(el)
        for el in token_list:
            if el[2] == 'EmptySpace':
                token_list.remove(el)
    return token_list

# get file name with productions, run test with productions string
if __name__ == '__main__':
    # grammar production rules
    f_g = open('grammar/MG1_with_begin_nesting.txt', 'r')
    # scanner code ending with EOF symbol = '$'
    f_s = open('scanner/code_begins2.txt', 'r')
    prods = f_g.read()
    user_code = f_s.read()

    # pass to the tester
    test(prods, user_code)

