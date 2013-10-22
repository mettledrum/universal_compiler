# Andrew Hoyle

# runs the sc on user input that represents code

from ScannerClass import *

def test(test_code):  
    sc = ScannerClass(test_code)

    # list to hold the output for error checking
    scan_out = []

    # run UNTIL EOF symbol found
    # NOTE: returns triple of info about token passed
    while sc.code[0] != '$':
        scan_out.append(sc.Scanner())

    # show list of tokens
    print scan_out

if __name__ == '__main__':
	# NOTE: customize input file
    #user_code = raw_input("type code: ")
    # this file has the example from class #15
    f = open('code1.txt', 'r')
    user_code = f.read()
    print(user_code)
    test(user_code)
