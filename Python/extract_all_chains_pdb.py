import sys
input_file = sys.argv[1]
pdb_file = open(input_file, 'r')
index = pdb_file.find('ATOM      1')
print index
