'''
    File:           count_atoms_pdbx.py
    Author:         Christina Lyu
    Date created:   5/15/17
    Updates:
    Last modified:  5/18/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a pdbx file
    Run format:     python count_atoms_pdbx.py pathToInputCifFile pathToOutputTextFile
    Run example:    python count_atoms_pdbx.py /Users/xxx/abc.cif /Users/xxx/
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
    extension = filename.split('.')[1]
    if extension.find('pdb') != -1:
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
    else:
        sys.stderr.write('Given file type wrong!')
main()
    
    

