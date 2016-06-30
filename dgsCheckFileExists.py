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
parser.add_argument('-i','--input', help='CSV file path contains list of code of works.', required=True)
parser.add_argument('-t','--targetpath', help='Target path contains original files need to be searched.', required=True )
parser.add_argument('-o','--output', help='CSV file with a list of existing files abs paths', required=True)
args = vars(parser.parse_args())

inputCSVPath = args['input']
outputFileListPath = args['output']
targetPath = args['targetpath']

print "输入编号列表：%s" % gbk2utf8(inputCSVPath)
print "输出文件绝对路径列表：%s" % gbk2utf8(outputFileListPath)
print "检测目标文件夹：%s" % gbk2utf8(targetPath)

print "##########################"

if not inputCSVPath or not outputFileListPath or not targetPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputFileListPath)[0] + '.log'
print "记录文件: %s" % gbk2utf8(logFilePath)
missingFilePath = os.path.splitext(outputFileListPath)[0]+'_missing.csv'
print "丢失文件列表: %s" % gbk2utf8(missingFilePath)

logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始检查文件。')

outputFileList = []
missingFileList = []



loadcsv(inputCSVPath)

for ele in csvtable:
    matches = []
    print "正在查找 %s" % ele[0].strip()
    for root,dirname,filenames in os.walk(targetPath):
        for filename in fnmatch.filter(filenames,ele[0].strip()+'*.*'):
            matches.append(os.path.join(root,filename))
    if not matches:
        #Output to missing list
        missingFileList.append(ele[0].strip())
        outstr = "文件不存在：编号 %s 未找到任何文件。" % ele[0].strip()
        print outstr
        logging.warning(outstr)
    else:
        print "OK"
        outputFileList += matches


#Check duplicated filenames in the output
basenameList = []
for item in matches:
    basenameList.append(os.path.basename(item))
dupList = [item for item, count in collections.Counter(basenameList).items() if count > 1]
for item in dupList:
    for ele in matches:
        if os.path.basename(ele) == item:
            outstr = ">>>文件 %s 存在重复<<<" % ele
            print outstr
            logging.warning(outstr)
            

             
#write out csv file

writecsv(outputFileList, outputFileListPath)

#write out missingFileList
writecsv(missingFileList, missingFilePath)
   










