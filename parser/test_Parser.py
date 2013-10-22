# Andrew Hoyle

# get class modules from sub-directories
from grammar.GrammarAnalyzerClass import GrammarAnalyzerClass
from scanner.ScannerClass import ScannerClass
#from ParserClass import ParserClass

# instantiates scanner, ga,
# passes CLEANED scanner list to parser
def test(prods, user_code_lines):
    # run the ga to populate its data members
    ga = GrammarAnalyzerClass(prods)
    ga.markLambda()
    ga.fillFirstSet()
    # NOTE: starting symbol for prod
    st_sym = "<systemGoal>"
    ga.fillFollowSet(st_sym)
    ga.fillPredictSet()
    ga.tableGenerator()

    # instantiate scanner
    sc = ScannerClass(user_code_lines)
    # list to hold the output for error checking
    scan_out = []
    # run UNTIL EOF symbol found
    # NOTE: returns triple of info about token passed
    while sc.code[0] != '$':
        scan_out.append(sc.Scanner()[2])

    # NOTE: cleans scanner list
    scan_out_clean = cleaner(scan_out)
    print scan_out_clean

    # give CLEANED scanner list to parser object

# cleans that list of junk using token names from scanner
# this should be a scanner function maybe
# gets rid of 'EmptySpace' and 'Comment'
def cleaner(token_list):
    while 'EmptySpace' in token_list:
        token_list.remove('EmptySpace')
    while 'Comment' in token_list:
        token_list.remove('Comment')
    return token_list

# get file name with productions, run test with productions string
if __name__ == '__main__':
    # grammar production rules
    f_g = open('grammar/MG1.txt', 'r')
    # scanner code
    f_s = open('scanner/code1.txt', 'r')
    prods = f_g.read()
    user_code = f_s.read()

    # pass to the tester
    test(prods, user_code)

