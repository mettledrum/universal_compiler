# Andrew Hoyle

# changes from parser to compiler are marked 
#  with "COMP#"

# COMP 
# helper class that is just a quadruple of index info
#  for the Compiler.PS data member
class EOP:
  def __init__(self, left, right, center, top):
    self.L = left
    self.R = right
    self.C = center
    self.T = top
  # printing
  def __str__(self):
    return "EOP("+str(self.L)+","+str(self.R)+","+str(self.C)+","+str(self.T)+")"
  def __repr__(self):
    return "EOP("+str(self.L)+","+str(self.R)+","+str(self.C)+","+str(self.T)+")"    

# COMP holds semantic information for SS
class SemRec:
  def __init__(self, n):
    n_str = str(n)
    if n_str == '+':
      self.extract = "add"
      self.kind = "OpRec"
    elif n_str == '-':
      self.extract = "sub"
      self.kind = "OpRec"
    else:
      self.extract = n_str
      self.kind = "ExprRec"
  # printing
  def __str__(self):
    return "SemRec("+self.extract+")"
  def __repr__(self):
    return "SemRec("+self.extract+")"


# has instance of grammarAnalyzer and Scanner
# NOTE: coupled with ga function names
class CompilerClass:

  # takes cleaned scanner token list and ga
  def __init__(self, cleaned_token_list, gramm_anal, write_stream):
    # NOTE: triple: (action #, buffer value, token_name)
    self.scan_list = cleaned_token_list
    self.ga = gramm_anal
    # COMP output for generated code
    self.out = open(write_stream, 'w')
    
    # stacks
    self.SS = []
    # COMP
    self.PS = []

    # COMP
    # NOTE: not sure about L and R... -1 maybe?
    # 0 indexing used here, and top must be an append,
    #  because trying to change a value at an idx that 
    #  doesn't exist throws an exception
    self.L = 0
    self.R = 0
    self.C = 0    
    self.T = 1                  # NOTE: just is len(PS)?  

    # NOTE: copied from ScannerClass and modified to do reverse
    self.token_dict = { 'PlusOp':'+', 'AssignOp':':=', 'Comma':',', 
                        'SemiColon':';', 'LParen':'(',
                        'RParen':')', 'MinusOp':'-', 'EOF':'$' }    

    # COMP - keeping track of temp names
    self.var_table = []
    self.temp_count = 0

    # COMP - simpler scanner list printing
    self.simple_scan_list = []
    for t in self.scan_list:
      self.simple_scan_list.append(t[1])


  # vars already instantiated in constructor
  def Start(self):
    return

  def Finish(self):
    self.out.write("halt")

  # add to var_table
  def Enter(self, s):
    self.var_table.append(s)

  # put in table and declare in machine code output IF hasn't been made yet
  def CheckId(self, s):
      if s not in self.var_table:
          self.Enter(s)
          self.out.write("declare " + s + " integer\n")

  # names temp vars put in SYMBOL_TABLE using GLOBAL TEMP_COUNTER
  def GetTemp(self):
    self.temp_count += 1
    _temp_name = "Temp&" + str(self.temp_count)
    self.CheckId(_temp_name)
    return _temp_name

  def Assign(self, sr_target, sr_source):
    self.out.write("store " + 
      self.SS[self.R + sr_source].extract + " " + 
      self.SS[self.R + sr_target].extract + '\n')

  def ReadId(self, sr):
    self.out.write("read " + 
      self.SS[self.R + sr].extract + 
      " integer\n")

  def WriteExpr(self, sr):
    self.out.write("write " + 
      self.SS[self.R + sr].extract + 
      " integer\n")

  # takes indices for referencing SS elems to change
  def GenInfix(self, op, e2):
    # temp val to be assigned to SS[L]
    _sr = SemRec(self.GetTemp())
    # get SemRecs from SS using idx values
    self.out.write(self.SS[self.R + op].extract + " " +
      self.SS[self.L].extract + " " +
      self.SS[self.R + e2].extract + " " +
      _sr.extract + 
      '\n')

    # assign temp back to self.L
    self.SS[self.L] = SemRec(_sr.extract)

  def ProcessId(self):
    self.CheckId(self.SS[self.C - 1].extract)
    self.SS[self.L] = SemRec(self.SS[self.C - 1].extract)

  def ProcessLiteral(self):
    self.CheckId(self.SS[self.C - 1].extract)
    self.SS[self.L] = SemRec(self.SS[self.C - 1].extract)

  # TODO: must get info from scanner?
  def ProcessOp(self):
    self.SS[self.L] = SemRec('+')

  # if v == -1, this means self.L
  def Copy(self, source_idx, target_idx):
    if target_idx == -1:
      self.SS[self.L] = SemRec(self.SS[self.R + source_idx].extract)
    else:
      self.SS[self.R + target_idx] = SemRec(self.SS[self.R + source_idx].extract)


  # uses the ga grammar table to find production table portion
  # pushes and pops on the SS
  # NOTE: system_goal has default
  def LLCompiler(self, start_symbol="<systemGoal>"):
    self.SS.append(start_symbol)

    # COMP0
    self.PS.append(start_symbol)

    # NOTE: debugging counter
    _counter = 0

    # work on SS recursively using ga lists/table
    while len(self.PS) != 0:
      # temp variables like pseudo code, lecture 15
      # COMP -1 is top of stack
      _X = self.PS[-1] 

      # COMP - prevents idx error
      if len(self.scan_list) != 0:
        _a = self.tokenLookUp(self.scan_list[0][2])
        _a_sem = self.tokenLookUp(self.scan_list[0][1])
      else:
        _a = '$'
        _a_sem = '$'

      # NOTE: debugging
      _counter += 1

      # NOTE: debugging print
      print "\nX:\t\t", _X
      print "a:\t\t", _a
      print "PS:\t\t", self.PS
      print "SS:\t\t", self.SS
      print "input:\t\t", self.simple_scan_list
      print "indices:\t", self.L, self.R, self.C, self.T

      # nonTerminal
      if _X in self.ga.nonTerms:
        # get production number to reference ga.prodList from table
        # key error will raise if not found
        _prod_numb = self.ga.predictTable[_X][_a]

        # NOTE: debugging prints
        print "non terminal"
        print "prod #: ", _prod_numb, "\tprod: ", self.ga.prodList[_prod_numb]
        print "RHS with actions: ", self.ga.RHS_with_actions[_prod_numb]

        # COMP1 pop X from PS
        self.PS.pop()

        # COMP2 push EOP on PS
        eop = EOP(self.L, self.R, self.C, self.T)
        self.PS.append(eop)

        # COMP3 push Ym,Ym-1,...,Y1 onto PS
        # temp list to hold symbols INCLUDING actions
        _reversePS = []
        # look up value in prodList
        for el in self.ga.RHS_with_actions[_prod_numb]:
          if el != 'lambda':                       # NOTE: must purge lambdas here
            _reversePS.append(el)
        # reverse append RHS to PS
        for i in range(len(_reversePS)):
          self.PS.append(_reversePS.pop())

        # COMP4 push NON action symbols onto SS
        #  in order y1,y2,...,ym
        # identify them as [^#] at beginning
        for el in self.ga.RHS[_prod_numb]:
          if el != 'lambda' and el[0] != '#':
            self.SS.append(el) 

        # COMP5 update the indices
        self.L = self.C
        self.R = self.T
        self.C = self.R
        self.T = len(self.SS)       # NOTE: count size of m'?

      # _X is in Terms, meaning it's a terminal symbol
      # underflow error could raise
      elif _X in self.ga.Terms:
        # debugging print
        print "terminal"

        if _a == _X:
          # COMP6
          _sr = SemRec(_a_sem)
          self.SS[self.C] = _sr
          # COMP7
          self.PS.pop()
          # COMP8
          self.scan_list = self.scan_list[1:]
          # COMP9
          self.C = self.C + 1
        # no match!
        else:
          print "syntax error"
          raise Exception

      # EOP
      # COMP
      elif isinstance(_X, EOP):
        # debugging
        print _X

        # COMP10
        # uses helper method
        self.restoreIdx(_X)

        # COMP11
        self.C = self.C + 1

        # COMP12
        self.PS.pop()


      # Action Symbol
      # COMP
      elif _X in self.ga.actions:
        # debugging print
        _method_str = _X[1:]
        print "action symbol:\t", _method_str

        # COMP13
        self.PS.pop()
        # COMP14 - calls the action symbols
        eval("self." + _method_str)

      # something weird COMP
      else:
        print "parse stack error, unknown type"
        raise Exception

      # NOTE: debugging print pause
      #if _counter == 5:
        #raw_input("pause")
        #_counter = 0

  # COMP - helper for restoring index values 
  def restoreIdx(self, eop):
    self.L = eop.L
    self.R = eop.R
    self.C = eop.C
    self.T = eop.T

  # helper function to switch between symbols and their symbol names
  def tokenLookUp(self, tok):
    # convert to token symbol names 
    if tok in self.token_dict:
      return self.token_dict[tok]
    else:
      return tok

