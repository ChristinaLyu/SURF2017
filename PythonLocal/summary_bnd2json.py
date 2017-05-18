# import os
# import sys
# import xml.etree.ElementTree
# from collections import OrderedDict
# import json
# def init_data():
#     data = OrderedDict()
#     data["Bnd : NrAtoms"] = 0
#     data["Bnd : NrBonds"] = 0
#     return data
#
# def parseBndFile(filename, data):
#     e = xml.etree.ElementTree.parse(filename).getroot()
#     for atomList in e.findall('atomList'):
#         data["Bnd:NrAtoms"] = int(atomList.get('nrAtoms'))
#     for bondList in e.findall('bondList'):
#         data["Bnd:NrBonds"] = int(bondList.get('nrBonds'))
#     return data
#
# def main():
#     print 'aaa'
#     filename = sys.argv[1]
#     path = sys.argv[2]
#     data = init_data()
#     data = parseBndFile(filename, data)
#     with open(path, 'w') as ofp:
#         json.dump(data, ofp, encoding = 'ascii')
# main()
#

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
    e = ET.parse(filename).getroot()
    
    for atomList in e.findall('atoms'):
        nrAtomsStr=atomList.get('nrAtoms')
        print 'nrAtomsStr=',nrAtomsStr
        data["Bnd:NrAtoms"] = int(atomList.get('nrAtoms'))
        data["Bnd:HasAtoms"] = True
        
    for bondList in e.findall('bonds'):
        data["Bnd:NrBonds"] = int(bondList.get('nrBonds'))
        data["Bnd:HasBonds"] = True
    return data
        
#--------------------------------------------------------   init_data  ----------
def init_data():

    data = OrderedDict()

    data["Summary:ProcessingError"] = False

    # Source file information
    data["FileSourceType"] = "bnd"
    data["File:Ext"] = "bnd"
    data["File:HasBadFormat"] = False
    data["File:NrFiles"] = 1
    
    # for .bnd xml file
    # STUB, but needs to be integrated
    data["Bnd:HasChains"] = False
    data["Bnd:NrChains"] = 0
    
    data["Bnd:HasAtoms"] = False
    data["Bnd:NrAtoms"] = 0
    
    data["Bnd:HasBonds"] = False
    data["Bnd:NrBonds"] = 0
    
    data["Bnd:NrBondsByType"] = {}
    
    
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
    data = makeBndSummary(inputBndFilePath, data)
    with open(outputJsonFilePath, 'w') as ofp:
        json.dump(data, ofp, encoding = 'ascii')

    debugMark(" END ", "summary_bbh2json.py")
#----------------------------------------------------------------------   Top level  ----------
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print ERROR_MESSAGE
        sys.exit(-1)

    main()

