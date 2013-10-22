# Andrew Hoyle
# 9/20/13
# Universal Scanner

# string.letters and string.digits for column indexing
import string

# takes the code string in constructor that has an EOF on it
# uses both a state table and action table to consume and
#  figure out the tokens
class ScannerClass:
    # takes string to be tokenized
    def __init__(self, code_string):
        # the code from user to be tokenized
        self.code = code_string

        # transition table
        # NOTE: extra EOF column added
        self.T = [ [ 1, 2, 3,14, 4,-1, 6,17,18,19,20,-1, 3, 3,-1,22],
                   [ 1, 1,11,11,11,11,11,11,11,11,11, 1,11,11,-1,22],
                   [12, 2,12,12,12,12,12,12,12,12,12,12,12,12,-1,22],
                   [13,13, 3,13,13,13,13,13,13,13,13,13, 3, 3,-1,22],
                   [21,21,21,21, 5,21,21,21,21,21,21,-1,21,21,-1,22],
                   [ 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,15, 5,22],
                   [-1,-1,-1,-1,-1,16,-1,-1,-1,-1,-1,-1,-1,-1,-1,22] ]

        # action table 
        # NOTE: blanks' text aren't captured, '' just returned
        # NOTE: extra EOF column added
        self.A = [ [ 2, 2, 3, 4, 2, 1, 2, 4, 4, 4, 4, 1, 3, 3, 1, 6],
                   [ 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6],
                   [ 6, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                   [ 6, 6, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 6, 6],
                   [ 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                   [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 6],
                   [ 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6] ]

        # for Scanner decisions
        self.action_dict = { 1:'Error', 2:'MoveAppend', 3:'MoveNoAppend',
                             4:'HaltAppend', 5:'HaltNoAppend', 6:'HaltReuse' }

        # numbers are keys to token names
        # NOTE: 22:'EOF' added
        self.token_dict = { 11:'Id', 12:'IntLiteral', 13:'EmptySpace',
                            14:'PlusOp', 15:'Comment', 16:'AssignOp',
                            17:'Comma', 18:'SemiColon', 19:'LParen',
                            20:'RParen', 21: 'MinusOp', 22:'EOF' }

        # reserved words table
        # NOTE: LookUpCode() will use it
        self.res_words = [ 'read', 'write', 'begin', 'end' ]

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
        elif cha == '$':            # NOTE: added EOF '$' recognition
            return 15
        else:
            return 14

    # return front char
    def CurrentChar(self):
        return self.code[0]

    # take off front char
    def ConsumeChar(self):
        self.code = self.code[1:]

    # consumes and returns [0]
    def Read(self):
        self.CurrentChar()
        self.ConsumeChar()

    # row major
    def NextState(self, state, char):
        return self.T[state][self.ColumnIdx(char)]

    # action table accessing
    def Action(self, state, cur_char):
        return self.action_dict[self.A[state][self.ColumnIdx(cur_char)]]

    # get final token integer code, I don't see how this
    #  from NextState
    def LookUpCode(self, state, char):
        return self.NextState(state, char)

    # see if token is in self.res_words[]
    def CheckExceptions(self, token_code, token_text):
        if token_text in self.res_words:
            print("reserved word:", token_text, "found")
            # NOTE: then make changes to token_code here
        return token_code

    # used for checking if word is reserved by Scanner
    # NOTE: changes token_name in triple to be the reserved word if
    #  found in self.res_word
    def ResCheck(self, token_to_check):
        if token_to_check in self.res_words:
            return True
        else:
            return False

    # action table and key drive its next move
    # state 0 means keep going, Scanner makes recursive call
    # NOTE: returns at triple with (token_code, text_from_buffer, token_name)
    def Scanner(self):
        # initial state
        state = 0
        token_text = ""

        while (True):
            current_action = self.Action(state, self.CurrentChar())
            # debugging
            #print "cur_char:\t", self.CurrentChar()
            #print " action:\t", current_action
            #print "  buffer:\t", token_text
            #print "   state:\t", state

            # lexical error
            if current_action == "Error":
                print("lexical error")
                raise Exception

            # not done yet
            elif current_action == "MoveAppend":
                state = self.NextState(state, self.CurrentChar())
                token_text = token_text + self.CurrentChar()
                self.ConsumeChar()

            elif current_action == "MoveNoAppend":
                state = self.NextState(state, self.CurrentChar())
                self.ConsumeChar()

            # halt return token
            elif current_action == "HaltAppend":
                token_code = self.LookUpCode(state, self.CurrentChar())
                token_text = token_text + self.CurrentChar()
                token_code = self.CheckExceptions(token_code, token_text)
                self.ConsumeChar()
                if token_code == 0:
                    (token_code, token_text) = self.Scanner()
                #print self.token_dict[token_code]
                # NOTE: checks res_word, changes third part of tuple if True
                if self.ResCheck(token_text):
                    return (token_code, token_text, token_text)
                else:
                    return (token_code, token_text, self.token_dict[token_code])

            elif current_action == "HaltNoAppend":
                token_code = self.LookUpCode(state, self.CurrentChar())
                token_code = self.CheckExceptions(token_code, token_text)
                self.ConsumeChar()
                if token_code == 0:
                    (token_code, token_text) = self.Scanner()
                #print self.token_dict[token_code] 
                # NOTE: checks res_word, changes third part of tuple if True
                if self.ResCheck(token_text):
                    return (token_code, token_text, token_text)
                else:
                    return (token_code, token_text, self.token_dict[token_code])

            elif current_action == "HaltReuse":
                token_code = self.LookUpCode(state, self.CurrentChar())
                token_code = self.CheckExceptions(token_code, token_text)
                if token_code == 0:
                    (token_code, token_text) = self.Scanner()
                #print self.token_dict[token_code]
                # NOTE: checks res_word, changes third part of tuple if True
                if self.ResCheck(token_text):
                    return (token_code, token_text, token_text)
                else:
                    return (token_code, token_text, self.token_dict[token_code])

            # just in case
            else:
                print("action table has wrong value")
                raise Exception




