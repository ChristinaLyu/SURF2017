'''
    File:           count_atoms_mmcif.py
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
    extension = filename.split('.')[1]
    if extension == 'cif':
        file = open(filename, 'r')
        file = file.read()
        index_1 = file.find('_atom_site.pdbx_PDB_model_num ')
        index_2 = file.find('_pdbx_poly_seq_scheme.asym_id')
        file = file[index_1 : index_2]
        index_4 = file.find('#')
        file = file[:index_4]
        file = file.splitlines()
        lastAtom = file[-1]
        nrAtoms = lastAtom.split()[1]
        
        nrFile = open(outPath, 'w')
        nrFile.write(nrAtoms)
        nrFile.close()
    else:
        sys.stderr.write("Given file type wrong!")
        
main()
    
    
