'''
    File:           count_atoms_pdbxgz.py
    Author:         Christina Lyu
    Date created:   5/15/17
    Updates:
    Last modified:  5/17/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a pdbx.gz file
    Run format:     python count_atoms_pdbxgz.py pathToInputCifFile pathToOutputTextFile
    Run example:    python count_atoms_pdbxgz.py /Users/xxx/abc.pdbx.gz /Users/xxx/
'''

import os
import sys



#JMOL get path to Jmol.jar
JMOL = '/Users/ChristinaLyu/Desktop/Summer2017/External/JmolData.jar'
filename = sys.argv[1]

outfile = sys.argv[2]
out = outfile.split('/')
out = out[ : -1]
outfolder = '/'.join(out)
File = open(outfile, 'w')
if not os.path.exists(outfolder):
    os.system('mkdir '+ outfolder)

os.system('java -jar /Users/ChristinaLyu/Desktop/Summer2017/External/Jmol.jar -no  -j "load ' + filename + ' ; select all ; getproperty atomInfo;"  > ' + outfolder + '/atominfo_large.txt')
atomInfoName =  outfolder + '/atominfo_large.txt'
atomInfofile = open(atomInfoName, 'r')

atomInfo = atomInfofile.read().splitlines()

nrAtoms = 0
for line in atomInfo:
    if line.find('*List') != -1:
        par = 'atomInfo	*List['
        par2 = ']'
        line = line.replace(par, '')
        line = line.replace(par2, '')
        nrAtoms = int(line)
File.write(str(nrAtoms))
