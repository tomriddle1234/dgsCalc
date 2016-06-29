# encoding=utf8

#According to file list move files from target folder to organised folders.

import fixutf8
import sys,os
import logging
import fnmatch
import argparse
import collections
import re
import shutil
import pandas
from dgsConstants import *
from dgsUtil import *


parser = argparse.ArgumentParser(description='This program is to fetch all detail xlsx file to compose a single big one. ')
parser.add_argument('-fp','--frompath', help='From path contains original files need to be moved.', required=True )
parser.add_argument('-o','--output', help='Output big table file path.', required=True )
args = vars(parser.parse_args())

fromPath = args['frompath']
outputPath = args['output']

print "来源文件夹：%s" % gbk2utf8(fromPath)
print "目标明细表文件：%s" % gbk2utf8(outputPath)

print "##########################"

if not fromPath or not outputPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputPath)[0] + '.log'
print "记录文件: %s" % gbk2utf8(logFilePath)


logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始组合明细表。')

#Create file list
formFileList = [] 
for root,dirname,filenames in os.walk(fromPath):
    for pattern in ['.xls','.xlsx']:
        for filename in fnmatch.filter(filenames,utf82gbk('*明细表*' + pattern)):
            formFileList.append(os.path.join(root,filename))
            outstr = "找到 %s" % formFileList[-1]
            print outstr
            logging.warning(outstr)
            

#Start load xlsx file with pandas
frames = []
skipCount = 0
for xlFile in formFileList:
    if os.path.isfile(xlFile):
        wf = pandas.ExcelFile(xlFile)
        ws = wf.parse("作品明细表")
        
        if ws.empty:
            outstr = ">>>未找到作品明细表 %s<<<" % xlFile
            print outstr
            logging.warning(outstr)
            skipCount += 1
            continue
        
        
        #check if this is old form
        oldFlag = False
        #print ws.iloc[0]
        for word in ws.iloc[0]:
            if type(word) == type(' '):
                if "师2" in word:
                    oldFlag = True
        if oldFlag:
            outstr = ">>>此表是旧表,跳过 %s<<<" % xlFile
            print outstr
            logging.warning(outstr)
            skipCount += 1
            continue
        
        
        #set the second row as the column names
        ws.columns = ws.iloc[0]
        
        #now have to drop last indecies, and the first one, cause it's the column name
        droprows = [0]
        finishFlag = False 
        for index, row in ws.iterrows():
            if not finishFlag:
                if pandas.isnull(row[0]) or row[0] == "汇总":
                    #from this index to the last
                    for c in range(index, ws.shape[0]):
                        droprows.append(c)
                        finishFlag = True
        droprows = list(set(droprows))
        print droprows
        ws.drop(ws.index[droprows],inplace=True)
        
        
        frames.append(ws)
    else:
        outstr = ">>>文件不存在 %s<<<" % xlFile
        print outstr
        logging.warning(outstr)
        skipCount += 1

if frames == []:
    outstr = ">>>未收集到任何表格,终止<<<"
    print outstr
    logging.warning(outstr)
    sys.exit()

result = pandas.concat(frames)
writer = pandas.ExcelWriter(outputPath)
result.to_excel(writer,u"作品明细表")
writer.save()

outstr = "跳过文件总数 %d" % (skipCount)
print outstr
logging.info(outstr)

logging.info('合并完毕。')
