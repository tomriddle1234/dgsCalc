# encoding=utf8

#input is a csv file path, and a search target folder
import fixutf8
import sys,os
import logging
import fnmatch
import argparse
import collections
from dgsUtil import *

parser = argparse.ArgumentParser(description='This program is to check file existence for DGS. Also generating a log file with the name of the output, end with .log ')
parser.add_argument('-i','--input', help='Total CSV file path.', required=True)
parser.add_argument('-o','--output', help='Video CSV file list.', required=True)
args = vars(parser.parse_args())

inputCSVPath = args['input']
outputVideoFileListPath = args['output']

print "输入编号列表：%s" % gbk2utf8(inputCSVPath)
print "输出文件绝对路径列表：%s" % gbk2utf8(outputVideoFileListPath)

print "##########################"

if not inputCSVPath or not outputVideoFileListPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputVideoFileListPath)[0] + '.log'
print "记录文件: %s" % gbk2utf8(logFilePath)

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











