# Andrew Hoyle

# runs the sc on user input that represents code

from ScannerClass import *

def test(test_code):  
    sc = ScannerClass(test_code)
    # run UNTIL EOF symbol found
    while sc.code[0] != '$':
        print(sc.Scanner())

if __name__ == '__main__':
    user_code = raw_input("type code: ")
    #print(user_code)
    test(user_code + '$')
