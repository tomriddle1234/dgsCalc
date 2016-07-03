# encoding=utf8

#input is a csv file path, and a search target folder
import fixutf8
import sys,os
import logging
import argparse
import collections
from dgsUtil import *
import re
import random 
import shutil
import csv


parser = argparse.ArgumentParser(description='This program is to move all the given list of file in to encoded filename.')
parser.add_argument('-i','--input', help='CSV File to load in file.', required=True)
parser.add_argument('-lp','--loadpath', help='File to be processed folder.', required=True)
parser.add_argument('-fp','--targetpath', help='Copy file target folder', required=True)
args = vars(parser.parse_args())

inputFilePath = args['input']
loadPath = args['loadpath']
copyTargetPath = args['targetpath']

if not os.path.isdir(copyTargetPath):
    print "Target is not a dir."

#load a list of seleted code.

csvtable = []
# if not os.path.isfile(inputFilePath):
    # print "Input %s does not exist" % filename
# with open(inputFilePath,'r') as csvfile:
    # csvreader = csv.reader(csvfile, delimiter=' ')      
    # for row in csvreader:
        # csvtable.append(row)

f = open(inputFilePath, 'rb')

for line in f:
	csvtable.append(line.strip())
            
if csvtable == []:
    print "Error empty load file"
originFilePath = []

for dirname, dirnames, filenames in os.walk(loadPath):
    # print path to all filenames.
    for filename in filenames:
        if os.path.isfile(os.path.join(dirname, filename)):
            originFilePath.append(os.path.join(dirname, filename))

for code in csvtable[0]:
    for filepath in originFilePath:
        if code in filepath:
            try:
                print "Copying %s to %s " % (filepath, os.path.basename(filepath))
                shutil.copy(filepath,os.path.join(copyTargetPath,os.path.basename(filepath)))
            except:
                print "Copying problem, %s -> %s" % (filepath, os.path.basename(filepath))
                
                







