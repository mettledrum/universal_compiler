# Andrew Hoyle

# has instance of grammarAnalyzer and Scanner
# NOTE: coupled with ga function names
class ParserClass:

  # takes cleaned scanner token list and ga
  def __init__(self, cleaned_token_list, gramm_anal):
    # triple
    self.scan_list = cleaned_token_list
    self.ga = gramm_anal
    self.stack = []

    # NOTE: copied from ScannerClass and modified to do reverse
    self.token_dict = { 'PlusOp':'+', 'AssignOp':':=', 'Comma':',', 
                        'SemiColon':';', 'LParen':'(',
                        'RParen':')', 'MinusOp':'-', 'EOF':'$' }    

  # helper function to switch between symbols and their symbol names
  def tokenLookUp(self, tok):
    # convert to token symbol names 
    if tok in self.token_dict:
      return self.token_dict[tok]
    else:
      return tok

  # uses the ga grammar table to find production table portion
  # pushes and pops on the stack
  # NOTE: sytem_goal has default
  def LLDriver(self, start_symbol="<systemGoal>"):
    self.stack.append(start_symbol)

    # work on stack recursively using ga lists/table
    while len(self.stack) != 0:
      # temp variables like pseudo code, lecture 15
      _X = self.stack.pop()
      _a = self.tokenLookUp(self.scan_list[0][2])

      print "X: ", _X, "\ta: ", _a

      # nonTerminal check, put on stack in reverse order
      if _X in self.ga.nonTerms:
        # get production number to reference ga.prodList from table
        # key error will raise if not found
        _prod_numb = self.ga.predictTable[_X][_a]

        # NOTE: debugging prints
        print _prod_numb
        print self.ga.prodList[_prod_numb]
        print self.ga.RHS[_prod_numb]

        # temp list to hold symbols
        _right_side = []
        # look up value in prodList
        for el in self.ga.RHS[_prod_numb]:
          if el != 'lambda':                       # NOTE: must purge lambdas here
            _right_side.append(el)
        # reverse append RHS to stack
        for i in range(len(_right_side)):
          self.stack.append(_right_side.pop())

        # oust the lambdas, (they mean NOTHING here)


        # NOTE: debugging print
        print "stack: ", self.stack, "\n"

        #raw_input("pause")

      # _X is in Terms, meaning it's a terminal symbol
      # underflow error could raise
      else:
        if _a == _X:
          print "scan_list BEFORE pop:", self.scan_list
          self.scan_list = self.scan_list[1:]
          print "scan_list after pop:", self.scan_list, '\n'
        # no match!
        else:
          print "syntax error"
          raise Exception
