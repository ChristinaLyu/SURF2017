'''
    File:           count_atoms_mmcif_lines.py
    Author:         Christina Lyu
    Date created:   5/15/17
    Updates:
    Last modified:  5/15/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a mmCIF file
    Run format:     python count_atoms_mmcif.py pathToInputCifFile pathToOutputTextFile
    Run example:    python count_atoms_mmcif.py /Users/xxx/abc.cif /Users/xxx/
'''

import os, sys
DEBUG = True
#-----------------------------------------------------------------      Utilities for debugging    ------
def debugMark(message,functionName):
    if DEBUG:
        print(' ')
        print('===============' + message + '  ' + functionName + '===============')
        print(' ')

def debugFun(message,functionName):
    if DEBUG:
        print('............' + message + '  ' + functionName)
        
def debugVar(var,val):
    if DEBUG:
        print(var + " = " + val)
        
#------------------------------------------------------------------ main
def main():
    filename = sys.argv[1]
    outPath = sys.argv[2]
    file = open(filename, 'r')
    file = file.read()
    nrAtoms = 0
    while file.find('MODEL        ') != -1 and file.find('ENDMDL') != -1:        
        index_1 = file.find('MODEL        ')
        index_2 = file.find('ENDMDL')
        cut = file[index_1: index_2 + 8]
        cut = cut.splitlines()
        cut = cut[1:-2]
        nrAtoms = nrAtoms + len(cut)
        file = file[index_2 + 8: ]
           
    nrFile = open(outPath, 'w')
    nrFile.write(str(nrAtoms))
    nrFile.close()
main()
    
    
