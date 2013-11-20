# Andrew Hoyle

# symbol table incorporating custom has function
class SymbolTable:
	def __init__(self, size):
		# mod for hash function "circling"
		self.m = size

		# instantiate list of stacks
		self.h_table = []
		for i in range(0,size):
			_stack = []
			self.h_table.append(_stack)

		self.pos = 0
		self.string_space = []
		self.block_depth = 1

	def hash_idx(self, st):
		# value from hash function
		_h_idx = 0
		# add ascii to value, mod by hash size
		for ch in list(st):
			_h_idx += ord(ch)
		_h_idx = _h_idx % self.m
		return _h_idx	

	def insert_st(self, st):
		# get hash index
		_h_val = self.hash_idx(st)

		# push triple of information into hash
		# (st_beg_idx, st_len, block_depth)
		self.h_table[_h_val].append((self.pos, len(st), self.block_depth))

		# put string into string space, char by char :(
		for ch in list(st):
			self.string_space.append(ch)

		# change string space write position to end+1
		self.pos = len(self.string_space)

	def push_block(self):
		# inc block depth counter
		self.block_depth += 1

	# get rid of the vars in hash at popped block,
	#  decrement block counter
	def pop_block(self):
		# underflow error
		if self.block_depth == 1:
			raise Exception("underflow error in hash table")

		# deleting from hash table
		_min_string_idx = len(self.string_space)
		# iterate through hash
		for stack in self.h_table:
			# iterate through stack
			_del_us = []
			for trip in stack:
				# keep track of min, del elem
				if trip[2] == self.block_depth:
					if trip[0] < _min_string_idx:
						_min_string_idx = trip[0]
					_del_us.append(trip)
			# list of trips to remove
			for t in _del_us:
				stack.remove(t)

		# lower block depth
		self.block_depth -= 1
		# purge string space
		del self.string_space[_min_string_idx:]
		# reset string space
		self.pos = len(self.string_space)

	# boolean, checks to see of it exists in current
	#  block scope AND string space
	def look_up(self, st):
		for stack in self.h_table:
			for trip in stack:
				# values from triple
				_beg = trip[0]
				_len = trip[1]
				_dep = trip[2]
				# check depth
				if _dep == self.block_depth:
					# pull value from string space
					_str = ''.join(self.string_space[_beg:(_beg+_len)])
					# compare strings
					if _str == st:
						return True
		return False









