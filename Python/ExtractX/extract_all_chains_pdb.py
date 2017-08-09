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

    if len(sys.argv) != 3:
        print 'ERROR:extractProtein_jmol: usage: python extractProtein.py input_pdb_file output_folder'
        sys.exit(-1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    pdb_file = open(input_file, 'r')
    pdb_file = pdb_file.read()
    file_name = ntpath.basename(os.path.splitext(input_file)[0])
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
       
        index_1 = pdb_file.find('ATOM      1')
        atoms = pdb_file[index_1: ]
        while atoms.find('ATOM  ') != -1 and atoms.find('TER  ') != -1:
            index_2 = atoms.find('TER  ')
            chain = atoms[ :index_2]
            atoms = atoms[index_2: ]
            index_3 = atoms.find('ATOM  ')
            chain = chain + atoms[ :index_3]
            atoms = atoms[index_3: ]
            chainName = chain
            chainName = chain.splitlines()
            first = chainName[0]
            first = first.split(' ')
            while first.count('') != 0:
                first.remove('')
            chain_ind = first[4].lower()
            filename = os.path.join(output_folder,file_name+"_" + chain_ind + ".pdb")
            outfile = open(filename, 'w')
            outfile.write(chain)
            outfile.close()
        # os.system('java -XX:-UseGCOverheadLimit -jar '+JMOL_JAR+' -n -j '+"'"+'load '+input_file+'; select :*; x=write("PDB"); write VAR x "'+output_file+'";'+"'")
    except IOError:
        print "ERROR:extractProtein_jmol: error while running JMol and writing to file " + output_file
        sys.exit(-1)

