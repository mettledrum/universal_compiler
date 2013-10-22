
# has instance of grammarAnalyzer and Scanner
class ParserClass:

  # takes cleaned scanner token list
  def __init__(self, cleaned_token_list):
    self.scan_list = cleaned_token_list

  # uses the grammar table to find production table portion
  # pushes and pops on the stack
  # NOTE: uses the Scanner to get the next values
  def LLDriver(self, start_symbol):
    # put starting symbol into stack
    self.parserStack.append(start_symbol)
    #
    while len(self.parserStack) != 0:
      if self.parserStack[-1] in self.nonTerms:
        # temporarily holds elements from table
        _tempL = []
        # stuff list with elems
        for elem in self.predictTable[self.parserStack[-1]]:
          _tempL.append(elem)
        # reverse temp
        _tempL.reverse()

        # put into stack in reverse order
        for el in _tempL:
          self.parserStack.append(el)

        # stack top is a terminal symbol
        else:
