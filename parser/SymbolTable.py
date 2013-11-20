# Andrew Hoyle

# symbol table incorporating custom has function

class SymbolTable:
	def _init__(self, size):
		self.m = size

		# instantiate list of stacks
		self.h_table = []
		for i in range(0,size):
			_stack = []
			self.h_table.append(_stack)

		self.pos = 0
		self.string_space = []
		self.block_depth = 1

	def insert(self, st):
		_s = list(st)
		h_idx = 0
		# get ascii sum of string's chars
		for ch in _s:
			h_idx += ord(ch)
		h_idx = h_idx % self.m

		_st_len = len(st)

		# push triple of information into hash
		self.h_table.append[h_idx].push((self.pos, _st_len, self.block_depth))







