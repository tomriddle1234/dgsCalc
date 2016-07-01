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

def getEncode(bn, fl):
    for ele in fl:
        if bn == ele[0]:
            return ele[1]

parser = argparse.ArgumentParser(description='This program is to rename all the given list of file in to encoded filename.')
parser.add_argument('-lp','--loadpath', help='File to be processed folder.', required=True)
parser.add_argument('-fp','--targetpath', help='Copy file target folder', required=True)
parser.add_argument('-o','--output', help='Output csv, one column code, one column renamed name.', required=True)
args = vars(parser.parse_args())

loadPath = args['loadpath']
outputFileListPath = args['output']
copyTargetPath = args['targetpath']

print "源文件路径：%s" % gbk2utf8(loadPath)
print "输出原编码，新编码对应文件：%s" % gbk2utf8(outputFileListPath)
print "拷贝目标目录，%s" % gbk2utf8(copyTargetPath)

print "##########################"

problemList = []

if not loadPath or not outputFileListPath or not copyTargetPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputFileListPath)[0] + '.log'
print "记录文件: %s" % gbk2utf8(logFilePath)

logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始分析文件。')

generalFileList = []
codeTable = []

#list target folder files 
if not os.path.isdir(loadPath) or not os.path.isdir(copyTargetPath):
    print "Input folder path is not folder."

csvtable = []
for dirname, dirnames, filenames in os.walk(loadPath):
    # print path to all filenames.
    for filename in filenames:
        csvtable.append(os.path.join(dirname, filename))

#loadcsv(inputCSVPath)

for ele in csvtable:
    filepath = ele
    if  filepath.endswith('.rar') or \
        filepath.endswith('.RAR') or \
        filepath.endswith('.zip') or \
        filepath.endswith('.ZIP'):
        continue
    generalFileList.append(filepath)

	
encodeRandomList = random.sample(range(len(generalFileList)), len(generalFileList))

categoryTable = [5,6,1,2,4,3,8,7,10,9,13,12,11,15,14]
encodeSeriesCache = ""
#Now start to check duration
for videofile in generalFileList:
    #get file basename.
    filebasename = os.path.splitext(os.path.basename(videofile))[0].strip()
	extname = os.path.splitext(os.path.basename(videofile))[-1].strip()
    substrList = filebasename.split('-')
    #no series data
    #2010001a
    encodeList = []
    print substrList
    if substrList[0][0] == "B" or substrList[0][0] == "b":
        encodeList.append('2')
	if substrList[0][0] == "A" or substrList[0][0] == "a":
        encodeList.append('1')
	if substrList[0][0] == "C" or substrList[0][0] == "c":
        encodeList.append('3')
	if substrList[0][0] == "D" or substrList[0][0] == "d":
        encodeList.append('4')
	if substrList[0][0] == "E" or substrList[0][0] == "e":
        encodeList.append('5')
	if substrList[0][0] == "F" or substrList[0][0] == "f":
        encodeList.append('6')
	if substrList[0][0] == "G" or substrList[0][0] == "g":
        encodeList.append('7')
	if substrList[0][0] == "H" or substrList[0][0] == "h":
        encodeList.append('8')
		
    if int(substrList[0][-2:]):
        encodeList.append(str(categoryTable[int(substrList[0][-2:])-1]).zfill(2))
    
	
	#Here we have to manually change the series files
	encodeList.append(str(encodeRandomList[generalFileList.index(videofile)]).zfill(4))
    
	#series data
    sublistCount = len(substrList)
    if (sublistCount == 5):
		#check if last records is a series work
		
		if codeTable[-1] and encodeList[-1]:
			if (len(codeTable[-1][0].split('-')) == 5):
				encodeList[-1] = codeTable[-1][1][3:-1]
				
		#here must check all situations, for different categories
		
		#all swf check if there's fla, swf should behine fla
		if codeTable[-1] and encodeList[-1]:
			#check before file's basename
			currentIndex = generalFileList.index(videofile)
			if currentIndex != 0:
				checkBasenameBefore = os.path.splitext(os.path.basename(generalFileList[currentIndex - 1]))[0].strip() 
				# Same code with different extension
				if checkBasenameBefore == filebasename:
					encodeList[-1] = codeTable[-1][1][3:-1]
					
		if (substrList[-1] != '' and substrList[-1] != ' ' and substrList[-1].isdigit()):
			if (int(substrList[-1]) == 1):
				encodeList.append('a')
			if (int(substrList[-1]) == 2):
				encodeList.append('b')
			if (int(substrList[-1]) == 3):
				encodeList.append('c')
    
    codeTable.append([filebasename,''.join(encodeList)])

with open(outputFileListPath,'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter='|')
	for value in codeTable:
		csvwriter.writerow(value)


#Start copy file

for videofile in generalFileList:
    #get file basename.
    filebasename = os.path.splitext(os.path.basename(videofile))[0].strip()
    extname = os.path.splitext(videofile)[-1].strip()
    renameTarget = getEncode(filebasename,codeTable)
    #print videofile
    #print os.path.join(copyTargetPath,renameTarget+extname)
    try:
        shutil.copy(videofile, os.path.join(copyTargetPath,renameTarget+extname))
    except:
        outstr = "拷贝文件错误 %s" % videofile
        print outstr
        logging.warning(outstr)
    




