# Andrew Hoyle

from SimpleScannerClass import *

# demonstrates why an action table is also needed for Scanner... 
# in this example, the + and A are messed up by the blank spaces
#  because they are consumed in the blank token.
def test(test_code):
    # code to input to scanner
    #test_code = "--  \n          + A$"
    
    sc = SimpleScannerClass(test_code)
    # run UNTIL EOF symbol found
    while sc.CurrentChar() != '$':
        print(sc.Scanner())

if __name__ == '__main__':
    user_code = raw_input("type code: ")
    print(user_code)
    test(user_code  + '$')
