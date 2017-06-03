__author__ = 'Christina Lyu'

import sys
import os
   
# -----------------------------------------------------------------------------
# Extract all residues from an input pdb file
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to a .pdb file containing one or more PRO residues
#       outputFolder: path to the output folder where a ABC_n.pdb file will be created
# TODO: check what happens if there is no protein chain in the input file, or for dna, rna etc.
#
# Description: extracts only the atoms with all residues from the ATOM lines
# TODO: check if it retains the SEQRES and other lines from the input pdb file
# --------------------------------------------------------------------

JMOL_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'

pdbPath = sys.argv[1]
folderPath = sys.argv[2]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

residueList = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL', 'ASX', 'GLX', 'UNK']

try:
    for residue in residueList:
        outFile = folderPath + '/' + pdbInd + '_' + residue + '.pdb'
        os.system('java -XX:-UseGCOverheadLimit -jar ' + JMOL_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + residue + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'")
        file = open(outFile, 'r')
        newfile = file.read()
        if newfile == '':
            file.close()
            os.system('rm -f -- ' + outFile)
except IOError:
    sys.exit(-1)
