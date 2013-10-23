# Andrew Hoyle

# get class modules from sub-directories
from grammar.GrammarAnalyzerClass import GrammarAnalyzerClass
from scanner.ScannerClass import ScannerClass
from ParserClass import ParserClass

# instantiates scanner, ga,
# passes CLEANED scanner list to parser
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

    # NOTE: cleans scanner list
    scan_out_clean = cleaner(scan_out)
    print "\nscanner:\t", scan_out_clean, '\n'

    # give CLEANED scanner list to parser object
    par = ParserClass(scan_out_clean, ga)

    # run the driver
    par.LLDriver()
    print par.stack

# cleans that list of junk using token names from scanner
# this should be a scanner function maybe
# gets rid of 'EmptySpace' and 'Comment'
def cleaner(token_list):
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
    f_g = open('grammar/MG1.txt', 'r')
    # scanner code ending with EOF symbol = '$'
    f_s = open('scanner/code1.txt', 'r')
    prods = f_g.read()
    user_code = f_s.read()

    # pass to the tester
    test(prods, user_code)

