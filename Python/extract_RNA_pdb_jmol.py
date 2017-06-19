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
from pathDependencies import JMOLDATA_JAR
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print 'ERROR:extractProtein_jmol: usage: python extractProtein.py input_pdb_file output_folder'
        sys.exit(-1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    file_name = ntpath.basename(os.path.splitext(input_file)[0])
    # output_dir = os.path.dirname(output_file)
    output_file = os.path.join(output_folder,file_name+"_pr.pdb")
    print "output_file = " + output_file

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except OSError:
        print "ERROR:extractProtein_jmol: output folder does not exist and it could not be created."
        sys.exit(-1)

    # run jmol to get the _pr.pdb file
    
    try:
        os.system('java -XX:-UseGCOverheadLimit -jar '+JMOLDATA_JAR+' -n -j '+"'"+'load '+input_file+'; select RNA; x=write("PDB"); write VAR x "'+output_file+'";'+"'")
    except IOError:
        print "ERROR:extractProtein_jmol: error while running JMol and writing to file " + output_file
        sys.exit(-1)

