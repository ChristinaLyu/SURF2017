__author__ = 'Christina Lyu'

import sys
import os
   
# -----------------------------------------------------------------------------
# Extract certain residues from an input pdb file
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to a .pdb file containing one or more PRO residues
#       outputFolder: path to the output folder where a ABC_n.pdb file will be created
#       output_type: either 'Single' or 'Dataset'
#       fragment_type: 'Interval', 'Prefix' or 'Suffix'
#       begin_id and end_id for intervals of residue
# TODO: check what happens if there is no protein chain in the input file, or for dna, rna etc.
#
# Description: extracts only the atoms with all residues from the ATOM lines
# TODO: check if it retains the SEQRES and other lines from the input pdb file
# --------------------------------------------------------------------

#JMOLDATA_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/JmolData.jar'
from pathDependencies import JMOLDATA_JAR

pdbPath = sys.argv[1]
folderPath = sys.argv[2]
output_type = sys.argv[3]
fragment_type = sys.argv[4]
begin_id = sys.argv[5]
end_id = sys.argv[6]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

if (output_type != 'Single' and output_type != 'Dataset') or (fragment_type != 'Interval' and fragment_type != 'Prefix' and fragment_type != 'Suffix'):
    sys.exit(-1)

try:
    if output_type == 'Single':
        outFile = folderPath + '/' + pdbInd + '_' + begin_id + '_' + end_id + '.pdb'
        if fragment_type == 'Prefix':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + '1-' + end_id + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)
        if fragment_type == 'Suffix':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + begin_id + '- :* and protein' + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)
        if fragment_type == 'Interval':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + begin_id + '-' + end_id + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)

    if output_type == 'Dataset':
        tempFolderPath = folderPath + '/temp'
        if not os.path.exists(tempFolderPath):
            os.mkdir(tempFolderPath)
        outFile = tempFolderPath + '/' + pdbInd + '_' + begin_id + '_' + end_id + '.pdb'

        if fragment_type == 'Prefix':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + '1-' + end_id + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)
        if fragment_type == 'Suffix':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + begin_id + '- :* and protein' + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)
        if fragment_type == 'Interval':
            command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + begin_id + '-' + end_id + '; x=write("PDB"); write VAR x "' + outFile + '";' + "'"
            os.system(command)

        tempFile = open(outFile,'r')
        tempFile = tempFile.read()
        splited = tempFile.splitlines()
        resNo = '0'
        fileNo = 0

        for m in range(len(splited)):
            atom = splited[m]

            if atom[:4] == 'ATOM':
                clean = atom[23: ]
                spaceInd = clean.find(' ')
                resId = clean[ :spaceInd]
                if resNo != resId:
                    resNo = resId
                    newFileName = folderPath + '/' + pdbInd + '_' + resNo + '.pdb'
                    newFile = open(newFileName, 'w')
                    newFile.write(atom + '\n')
                    newFile.close()
                else:
                    existFileName = folderPath + '/' + pdbInd + '_' + resNo + '.pdb'
                    existFile = open(existFileName, 'a')
                    existFile.write(atom + '\n')
                    existFile.close()
except IOError:
    sys.exit(-1)

