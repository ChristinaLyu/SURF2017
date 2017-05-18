'''
    File:           summary_bnd2jsonFolder.py
    Author:         Ileana Streinu based on older wrapper code by John Bowers
    Date created:   22 Feb 2017
    Updates: 	    22 Feb 2017
    Last modified:  22 Feb 2017
    Python Version: 2.7

    Description:    computes a summary of a bnd file in a json format
                    output is a folder
                    the script sets the name of the json file, then invokes summary_bnd2json
    Run format:     python summary_bnd.py pathToInputPdbFile pathToOutputJsonFile
    Run example:    python summary_bnd.py /Users/xxx/1ABW.bnd /Users/xxx/abc.json
'''

import os, sys, subprocess

if len(sys.argv) < 3:
    print "USAGE: python summary.py [input-bnd-file-path] [output-folder-path]"
    sys.exit(-1)

in_path = sys.argv[1]   # a path to a .bnd file
# print "in_path = "+in_path
split_in_path=os.path.splitext(in_path)
input_file_path_and_name,ext=split_in_path

# print "ext = "+ext

if not ext =='.bnd':
    sys.exit(-1)
    
input_file_name = input_file_path_and_name.split('/')[-1]
out_folder_path = sys.argv[2]

# out_folder_path should always be a folder. A file named abc.json is created 
# in that folder, where abc.bnd is the input file

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
    out_path = out_folder_path + input_file_name + ".json"

# invoke the summary_wrapped code
subprocess.call(['python', path_to_script_folder + 'summary_bnd2json.py', in_path, out_path])
