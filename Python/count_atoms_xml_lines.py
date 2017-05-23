'''
    File:           count_atoms_xml_lines.py
    Author:         Christina Lyu
    Date created:   5/15/17
    Updates:
    Last modified:  5/18/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a xml file
    Run format:     python count_atoms_xml.py pathToInputCifFile pathToOutputTextFile
    Run example:    python count_atoms_xml.py /Users/xxx/abc.cif /Users/xxx/
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
def main(filename, outPath):
    extension = filename.split('.')[-1]
    
    if extension == 'xml':
        listtttt = []
        file = open(filename, 'r')
        file = file.read()
        index_1 = file.find('<PDBx:atom_site id="')
        index_2 = file.find('</PDBx:atom_siteCategory>')
        file = file[index_1 : index_2]
        lis = file.split('<PDBx:atom_site id="')
        nrAtom = len(lis)
        outFile = open(outPath, 'w')
        outFile.write(str(nrAtom))
    else:
        sys.stderr.write("Given file type wrong!")
        sys.exit(-1)
        
        # raise ValueError('Wrong extension')
        #sys.stderr.write("Given file type wrong!")

if __name__ == '__main__':
    filename = sys.argv[1]
    outPath = sys.argv[2]
    main(filename, outPath)
                
