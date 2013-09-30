# Andrew Hoyle

import string

# Just has a state table, but this IS NOT SUFFICIENT because it also needs
#  an action table because the current char is not supposed to always be
#  consumed.
# This is useful for action table debugging to make sure the right actions
#  are taken by the scanner... whether it advances or not.
class SimpleScannerClass:
    # takes string to be tokenized
    def __init__(self, code_string):
        self.code = code_string
        # transition table
        self.T = [ [1,2,3,14,4,-1,6,17,18,19,20,-1,3,3,-1],
                   [1,1,11,11,11,11,11,11,11,11,11,1,11,11,-1],
                   [12,2,12,12,12,12,12,12,12,12,12,12,12,12,-1],
                   [13,13,3,13,13,13,13,13,13,13,13,13,3,3,-1],
                   [21,21,21,21,5,21,21,21,21,21,21,-1,21,21,-1],
                   [5,5,5,5,5,5,5,5,5,5,5,5,5,15,5],
                   [-1,-1,-1,-1,-1,16,-1,-1,-1,-1,-1,-1,-1,-1,-1] ]

        # numbers are keys to token names
        self.token_dict = { 11:'Id', 12:'IntLiteral', 13:'EmptySpace',
                            14:'PlusOp', 15:'Comment', 16:'AssignOp',
                            17:'Comma', 18:'SemiColon', 19:'LParen',
                            20:'RParen', 21: 'MinusOp' }

    # action table, returns the index of the table
    def ColumnIdx(self, cha):
        if cha in string.letters:
            return 0
        elif cha in string.digits:
            return 1
        elif cha == ' ':
            return 2
        elif cha == '+':
            return 3
        elif cha == '-':
            return 4
        elif cha == '=':
            return 5
        elif cha == ':':
            return 6
        elif cha == ',':
            return 7
        elif cha == ';':
            return 8
        elif cha == '(':
            return 9
        elif cha == ')':
            return 10
        elif cha == '_':
            return 11
        elif cha == '\t':
            return 12
        elif cha == '\n':
            return 13
        else:
            return 14

    # return front char
    def CurrentChar(self):
        return self.code[0]

    # take off front char
    def ConsumeChar(self):
        self.code = self.code[1:]

    def Read(self):
        self.CurrentChar()
        self.ConsumeChar()

    # row major
    def NextState(self, state, char):
        return self.T[state][self.ColumnIdx(char)]

    def Scanner(self):
        state = 0
        
        while self.CurrentChar() != '$' and state < 11:
            next_state = self.T[state][self.ColumnIdx(self.CurrentChar())]
            # monitor its process
            print("char:", self.CurrentChar())
            print("n_st:", next_state)
            # check for errors
            if next_state == -1:
                print("lexical error")
                raise Exception
            state = next_state

            # next actions depend on states, SO THIS PART IS WHAT MESSES
            #  THINGS UP sometimes... 
            self.Read()

        # a "final" state is reached
        if state >= 11:
            return self.token_dict[state]
        # something screwy in table numbers
        else:
            print("table error")
            raise Exception


