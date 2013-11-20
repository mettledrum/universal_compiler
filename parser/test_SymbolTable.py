
from SymbolTable import SymbolTable

# loop for tinkering with class
def test():
	st = SymbolTable(3)

	# debugging print
	print "hash table:", st.h_table
	print "string space:", st.string_space
	print "write position:", st.pos
	print "block depth", st.block_depth, "\n"

	while (True):
		r = raw_input("pop/push/string: ")
		if r == "pop":
			st.pop_block()
		elif r == "push":
			st.push_block()
		else:
			st.insert_st(r)

		# debugging print
		print "hash table:", st.h_table
		print "string space:", st.string_space
		print "write position:", st.pos
		print "block depth", st.block_depth, "\n"
		print "a exists?: ", st.look_up('a')

if __name__ == '__main__':
	test()