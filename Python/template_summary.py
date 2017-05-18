'''
    File:           summary_bnd2json.py
    Author:         Ileana Streinu, with Christina Lyu
    Date created:   April 26, 2017
    Updates: 	    2017: Apr 26
    Last modified:  2017: Apr 26
    Python Version: 2.7

    Description:    computes a summary of a bnd file in a json format
    Usage:          python summary_bnd2json.py path_to_input_file.pdb path_to_output_file.bnd
'''

DEBUG = False
ERROR_MESSAGE = "ERROR:summary_bnd2json.py must be called with input: a bnd file path, output: a json file path. "


import StringIO, os, sys, json
import os.path, shutil

from collections import OrderedDict
from xml.etree import ElementTree as ET

#--------------------------------------------------      Utilities for debugging    ------
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
#--------------------------------------------------------   bbh Summary ---------
def makeBndSummary(filename, data):
    e = xml.etree.ElementTree.parse(filename).getroot()
    for atomList in e.findall('atomList'):
        data["Bnd:NrAtoms"] = int(atomList.get('nrAtoms'))
    for bondList in e.findall('BondList'):
        data["Bnd:NrBonds"] = int(bondList.get('nrBonds'))
    return data
        
#--------------------------------------------------------   init_data  ----------
def init_data():

    data = OrderedDict()

    data["Summary:ProcessingError"] = False

    # Source file information
    # data["File Source Type"] = "pdb"
    data["File:Ext"] = "bbh"
    data["File:HasBadFormat"] = False
    data["File:NrFiles"] = 1
    
    # for BBH (body-bar-hinge) xml file
    
    data["Bnd:NrAtoms"] = 0
    data["Bnd:NrBonds"] = 0
    
    
    # data['Bbh:NrActivePoints']="undefined"
    
    return data
#-------------------------------------------------------------------   MAIN  ----------
def main():

    debugMark(" START ", "summary_bbh2json.py")
    
    
    inputBndFilePath = sys.argv[1]
    debugVar("inputBndFilePath",inputBndFilePath)
    outputJsonFilePath = sys.argv[2]
    debugVar("outputJsonFilePath",outputJsonFilePath)
    
    data = init_data()
    data = makeBndSummary(filename, data)
    with open(outputJsonFilePath, 'w') as ofp:
        json.dump(data, ofp, encoding = 'ascii')

    debugMark(" END ", "summary_bbh2json.py")
#----------------------------------------------------------------------   Top level  ----------
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print ERROR_MESSAGE
        sys.exit(-1)

    main()

