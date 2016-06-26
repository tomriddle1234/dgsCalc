# encoding=utf8

#input is a csv file path, and a search target folder

import sys,os
import csv
import logging
import fnmatch

logging.basicConfig(filename='fileCheck.log', level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始检查文件。')

csvtable = []

outputFileList = []

#load csv file 

def loadcsv(filename):
    """
    load prepared csv file
    """
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')      
        for row in csvreader:
            csvtable.append(row)
            
def writecsv(data, filename,title=None):
    """
    write output csvfile
    data is a dict
    """
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        if title:
            csvwriter.writerow(title)
        for value in data:
                csvwriter.writerow([value])

loadcsv('prepared_filelist.csv')
targetPath = "."

for ele in csvtable:
    matches = []
    print "正在查找 %s" % ele[0]
    for root,dirname,filenames in os.walk(targetPath):
        for filename in fnmatch.filter(filenames,ele[0]+'*.*'):
            matches.append(os.path.join(root,filename))
    if not matches:
        outstr = "文件不存在：编号 %s 未找到任何文件。" % ele[0]
        print outstr
        logging.warning(outstr)
    else:
        print "OK"
        outputFileList += matches
        

#write out csv file


writecsv(outputFileList, 'fileCheckResult.csv')
    













