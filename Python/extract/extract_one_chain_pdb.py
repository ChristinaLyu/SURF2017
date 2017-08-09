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
JMOL_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print 'ERROR:extractProtein_jmol: usage: python extractProtein.py input_pdb_file output_folder'
        sys.exit(-1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    chainId = sys.argv[3]
    
    pdb_file = open(input_file, 'r')
    pdb_file = pdb_file.read()
    file_name = ntpath.basename(os.path.splitext(input_file)[0])

    pdbFile = input_file.split('/')[-1]
    pdbInd = pdbFile.split('.')[0]
    # output_dir = os.path.dirname(output_file)
    
    # print "output_file = " + output_file

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except OSError:
        print "ERROR:extractProtein_jmol: output folder does not exist and it could not be created."
        sys.exit(-1)

    # run jmol to get the _pr.pdb file
    
    try:
        outFileName = output_folder + '/' + pdbInd + '_' + chainId + '.pdb'
        outFile = open(outFileName, 'w')
        
        splited = pdb_file.splitlines()
        index_1 = 0
        for n in range(len(splited)):
            line = splited[n]
            if line[:5] == 'ATOM ':
                index_1 = n
                break

        atoms = splited[index_1: ]
        index_2 = 0
        terL = []
        for m in range(len(atoms)):
            line = atoms[m]
            if line[:4] == 'TER ':
                terL.append(m)
            if line[:5] != 'ATOM ' and line[:4] != 'TER ':
                index_2 = m
                break
        atoms = atoms[ :index_2 + 1]
        chainIndex = 0
        for k in terL:
            line = atoms[k]
            clean = line.split(' ')
            while clean.count('') != 0:
                clean.remove('')
            if clean[3] == chainId:
                chainIndex = k
                break

        terIndex = terL.index(chainIndex)
        if terIndex != 0:
            previousIndex = terL[terIndex - 1]
            chain = atoms[previousIndex + 1:chainIndex + 1]
        else:
            chain = atoms[ :chainIndex + 1]

        chain = '\n'.join(chain)
        outFile.write(chain)
        outFile.close()
            
    except IOError:
        print "ERROR:extractProtein_jmol: error while running JMol and writing to file " + output_file
        sys.exit(-1)

