# encoding=utf8

#input is a csv file path, and a search target folder
import fixutf8
import sys,os
import logging
import fnmatch
import argparse
import collections
from dgsUtil import *
import re
import subprocess



parser = argparse.ArgumentParser(description='This program is to check file existence for DGS. Also generating a log file with the name of the output, end with .log ')
parser.add_argument('-i','--input', help='Total CSV file path.', required=True)
parser.add_argument('-o','--output', help=' Video CSV file list.', required=True)
args = vars(parser.parse_args())

inputCSVPath = args['input']
outputVideoFileListPath = args['output']
outputVideoProblemFileListPath = ""

print "输入编号列表：%s" % gbk2utf8(inputCSVPath)
print "输出文件绝对路径列表：%s" % gbk2utf8(outputVideoFileListPath)

print "##########################"

problemList = []
def getLength(filename):
	try:
		number = subprocess.check_output("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"%s\"" % filename ,shell=True).strip()
	except:
		print "Execute Problem."
		problemList.append(filename)
		return 0.0
	if re.match("^\d+?\.\d+?$", number) is None:
		print number
		print "Not float"
		problemList.append(filename)
		return 0.0
	if number:
		print number
		return float(number)
	else:
		problemList.append(filename)
		return 0.0


if not inputCSVPath or not outputVideoFileListPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputVideoFileListPath)[0] + '.log'
print "记录文件: %s" % gbk2utf8(logFilePath)

outputVideoProblemFileListPath = os.path.splitext(outputVideoFileListPath)[0] + '_problem.csv'
print "问题文件: %s" % gbk2utf8(outputVideoProblemFileListPath)

logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始分析文件。')

videoFileList = []

loadcsv(inputCSVPath)

for ele in csvtable:
    filepath = ele[0].strip()
    if filepath.endswith('.pdf') or \
        filepath.endswith('.PDF') or \
        filepath.endswith('.mp3') or \
        filepath.endswith('.fla') or \
        filepath.endswith('.jpg') or \
        filepath.endswith('.doc') or \
        filepath.endswith('.docx') or \
        filepath.endswith('.docm') or \
        filepath.endswith('.DOCM') or \
        filepath.endswith('.rar') or \
        filepath.endswith('.RAR') or \
        filepath.endswith('.JPG') or \
        filepath.endswith('.DOC') or \
        filepath.endswith('.DOCX') or \
        filepath.endswith('.PPT') or \
        filepath.endswith('.PPTX') or \
        filepath.endswith('.ppt') or \
		filepath.endswith('.txt') or \
		filepath.endswith('.zip') or \
		filepath.endswith('.ZIP') or \
        filepath.endswith('.pptx'):
        continue
    videoFileList.append(filepath)

#write out csv file

writecsv(videoFileList, outputVideoFileListPath)
writecsv(problemList,outputVideoProblemFileListPath)

#Now start to check duration
#ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <>
timeSum = 0.0
fileCount = 0
for videoFile in videoFileList:
	if os.path.isfile(videoFile): #whatif file is missing
		fileDuration = getLength(videoFile)
		timeSum += fileDuration
		if fileDuration != 0.0:
			fileCount += 1
print timeSum
#As of 2016-06-30 result is around 18.5hours
#logging.info("播放总时间 %s, 可播放文件数 %d") % (str(timeSum),fileCount)
#write problem list









