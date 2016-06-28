# encoding=utf8

#According to file list move files from target folder to organised folders.

import fixutf8
import sys,os
import csv
import logging
import fnmatch
import argparse
import collections
import re
import shutil
from dgsConstants import *


#load csv file 
csvtable = []

codePattern = re.compile("^[A-H][0-1][0-9]-[2][0]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]")

def loadcsv(filename):
    """
    load prepared csv file
    """
    if not os.path.isfile(filename):
        print "Input %s does not exist" % filename
        return
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')      
        for row in csvreader:
            csvtable.append(row)

parser = argparse.ArgumentParser(description='This program is to move files from target folder to organised folders. ')
parser.add_argument('-i','--input', help='CSV file path contains list of abs file path.', required=True)
parser.add_argument('-fp','--frompath', help='From path contains original files need to be moved.', required=True )
parser.add_argument('-t','--targetpath', help='Target path contains that will be organised.', required=True )
args = vars(parser.parse_args())

inputCSVPath = args['input']
fromPath = args['frompath']
targetPath = args['targetpath']

print "输入文件绝对路径列表：%s" % inputCSVPath
print "来源文件夹：%s" % fromPath
print "目标文件夹：%s" % targetPath

print "##########################"

if not inputCSVPath or not fromPath or not targetPath:
    print "Input argument Error."

logFilePath = os.path.join(targetPath,'move.log')
print "记录文件: %s" % logFilePath


logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始搬运文件。')

#load abs folders
loadcsv(inputCSVPath)

#Base on the code, send the files to separated folders.
# 命题类别/命题名称/命题文件

skipCount = 0
count = 0
for abspath in csvtable:
    #get basename
    #Check code.
    codename = os.path.splitext(os.path.basename(abspath))[0]
    extname = os.path.splitext(os.path.basename(abspath))[-1]
    #jump out pdf files
    if extname == ".pdf" or extname == ".PDF":
        print "跳过PDF文件：%s" % abspath
    
    if not codePattern.match(codename):
        outstr = "文件编号格式不正确,不搬运。%s" % abspath
        print outstr
        logging.warning(outstr)
        skipCount += 1
        continue
    
    subCodeStrList = codename.split('-')
    
    firstSubStr = subCodeStrList[0]
    
    categoryStr = firstSubStr[0]
    themeStr = firstSubStr[-2:]
    
    
    if not categoryStr in categoryNoList:
        outstr = "类别代码不再类别池中,不搬运。%s" % categoryStr
        print outstr
        logging.warning(outstr)
        skipCount += 1
        continue
    elif not themeStr in themeNoList:
        outstr = "命题名称代码不再池中,不搬运。%s" % themeStr
        print outstr
        logging.warning(outstr)
        skipCount += 1
        continue
    else:
        targetCategoryDirStr = os.path.join(targetPath,categoryList[categoryNoList.index(firstSubStr)])
        #Create bunch of folders
        #if there's no directory, create one
        if not os.path.isdir(targetCategoryDirStr):
            try:
                os.mkdirs(targetCategoryDirStr)
            except:
                outstr = "无法创建目录 %s" % targetCategoryDirStr
                print outstr
                logging.warning(outstr)
                skipCount += 1
                continue
        targetThemeDirStr = os.path.join(targetCategoryDirStr, themeList[themeNoList.index(int(themeStr))])
        if not os.path.isdir(targetThemeDirStr):
            try:
                os.mkdirs(targetThemeDirStr)
            except:
                outstr = "无法创建目录 %s" % targetThemeDirStr
                print outstr
                logging.warning(outstr)
                skipCount += 1
                continue
        # Move file
        try:
            shutil.move(abspath,os.path.join(targetThemeDirStr,os.path.basename(abspath)))
        except:
            outstr = "无法移动文件 %s --> %s" % (abspath, os.path.join(targetThemeDirStr,os.path.basename(abspath)))
            print outstr
            logging.warning(outstr)
            skipCount += 1
            continue
        
    count += 1
        
        
     
outstr = "输入文件总数 %d 跳过文件总数 %d" % (count, skipCount)
print outstr
logging.info(outstr)

loggin.info('搬运完毕。')
