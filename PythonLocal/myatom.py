#Test
#myatom.py
#file to import xml format and count the atom number
from Bio import PDB
import os
import sys
def main():
    filename = sys.argv[1]
    print(filename)
    parser = PDB.PDBParser()
    atomnumber = 0
    structure = parser.get_structure('PDB file', filename)
    for model in structure:
        for chain in model:
            print(chain)
            for residue in chain:
                print(residue.resname, residue.id[1])
                for atom in residue:
                    print(atom.name, atom.get_serial_number())
                    atomnumber = atomnumber + 1
                
    print('atomnumber = ', atomnumber)
   
            
                

main()
