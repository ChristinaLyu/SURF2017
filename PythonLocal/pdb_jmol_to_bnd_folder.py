'''
    File:           pdb_jmol_to_bnd_folder.py
    Author:         Ileana Streinu
    Date created:   4/26/17
    Updates: 	    
    Last modified:  4/26/17
    Python Version: 2.7

    Description:    creates a bnd file in the output folder and runs pdb_jmol_to_bnd.py
    Run format:     python pdb_jmol_to_bnd_folder.py pathToInputPdbFile pathToOutputJsonFolder
    Run example:    python pdb_jmol_to_bnd_folder.py /Users/xxx/abc.pdb /Users/xxx/
'''

import os, sys, subprocess

if len(sys.argv) < 3:
    print "USAGE: python pdb_jmol_to_bnd_folder.py [input-pdb-file-path] [output-folder-path]"
    sys.exit(-1)

in_path = sys.argv[1]   
split_in_path=os.path.splitext(in_path)
input_file_path_and_name,ext=split_in_path

if not ext =='.pdb':
    sys.exit(-1)
    
input_file_name = input_file_path_and_name.split('/')[-1]
out_folder_path = sys.argv[2]

# out_folder_path should always be a folder. A file named abc.bnd is created 
# in that folder, where abc.pdb is the input file

if not os.path.isfile(in_path):
    if in_path[-1] != '/':
        in_path_dir = in_path + '/'
        
# this is done to facilitate invoking the summary_wrapped script
# this should be eventually deprecated
path_to_script_folder = os.path.dirname(os.path.realpath("__file__"))
if path_to_script_folder[-1] != '/':
    path_to_script_folder += '/'

# set up the name and path for the output summary file    
if not os.path.isfile(out_folder_path):
    if out_folder_path[-1] != '/':
        out_folder_path = out_folder_path + "/"
    out_path = out_folder_path + input_file_name + ".bnd"

# invoke the summary_wrapped code
subprocess.call(['python', path_to_script_folder + 'pdb_jmol_to_bnd.py', in_path, out_path])
