__author__ = 'Christina Lyu'

import sys
import os
import ntpath

##from ConfigParser import SafeConfigParser
##config = SafeConfigParser()
##config.read('../../../Settings/configrebecca.ini')
##if config.has_section('paths'):
##    JMOL_JAR = os.path.abspath(config.get('paths', 'path_to_jmol_jar_from_bin_bio_extract'))
##    
# -----------------------------------------------------------------------------
# Extract the protein from an input pdb file using JMol
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to a .pdb file containing one or more protein chains
#       outputFolder: path to the output folder where a _pr.pdb file will be created
# TODO: check what happens if there is no protein chain in the input file, or for dna, rna etc.
#
# Description: extracts only the CA atoms from the ATOM lines
# TODO: check if it retains the SEQRES and other lines from the input pdb file
#       in principle, it should. It should just discard the non-CA atom lines.
# --------------------------------------------------------------------
#JMOL_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print 'ERROR:extractProtein_jmol: usage: python extractProtein.py input_pdb_file output_folder'
        sys.exit(-1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    pdb_file = open(input_file, 'r')
    pdb_file = pdb_file.read()
    splited = pdb_file.splitlines()
    
    file_name = ntpath.basename(os.path.splitext(input_file)[0])
    pdbFile = input_file.split('/')[-1]
    pdbInd = pdbFile.split('.')[0]

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except OSError:
        print "ERROR:extractProtein_jmol: output folder does not exist and it could not be created."
        sys.exit(-1)
    
    try:
        outFileName = output_folder + '/' + pdbInd + '_dna.pdb'
        outFile = open(outFileName, 'w')
        outFile.close()

        index_1 = 0
        resL = ['DA', 'DT', 'DG', 'DC']
               
        dnaAtoms = []
        for n in range(len(splited)):
            line = splited[n]
            if line[ :5] == 'ATOM ':
                res = line[18:20]
                if resL.count(res) != 0:
                    dnaAtoms.append(line)
            if line[ :7] == 'MODEL ':
                dnaAtoms.append(line)
            if line[ :8] == 'ENDMOL ':
                dnaAtoms.append(line)
        atomNo = 0
        for m in range(len(dnaAtoms)):
            line = dnaAtoms[m]
            outFile = open(outFileName, 'a')
            if line[ :5] == 'ATOM ':
                atomNo = atomNo + 1
                atomIn = str(atomNo)
                line = line[ :5] + (6-len(atomIn)) * ' ' + atomIn + line[11:]
                outFile.write(line + '\n')
                chainId = line[21]
                if m != len(dnaAtoms) -1:
                    nextL = dnaAtoms[m + 1]
                    nextChain = nextL[21]
                lineRes = line[18:26]
                if chainId != nextChain or m == len(dnaAtoms) - 1:
                    atomNo = atomNo + 1
                    atomIn = str(atomNo)
                    terLine = 'TER  ' + (6 - len(atomIn)) * ' ' + atomIn + 7 * ' ' + lineRes
                    outFile.write(terLine + '\n')
            else:
                outFile.write(line)


    except IOError:
        print "ERROR:extractProtein_jmol: error while running JMol and writing to file " + output_file
        sys.exit(-1)

