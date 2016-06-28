# encoding=utf8

#According to file list move files from target folder to organised folders.

import fixutf8
import sys,os
import csv
import logging
import fnmatch
import argparse
import collections

from dgsConstants import *

#load csv file 

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
frompath = args['frompath']
targetPath = args['targetpath']

print "输入文件绝对路径列表：%s" % inputCSVPath
print "来源文件夹：%s" % frompath
print "目标文件夹：%s" % targetPath

print "##########################"

if not inputCSVPath or not frompath or not targetPath:
    print "Input argument Error."

logFilePath = os.path.join(targetPath,'move.log')
print "记录文件: %s" % logFilePath


logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始搬运文件。')

#load abs folders



#Base on the code, send the files to separated folders.

#Check code.

#Create bunch of folders


loggin.info('搬运完毕。')
