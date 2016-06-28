# encoding=utf8

#input is a csv file path, and a search target folder
import fixutf8
import sys,os
import csv
import logging
import fnmatch
import argparse
import collections

parser = argparse.ArgumentParser(description='This program is to check file existence for DGS. Also generating a log file with the name of the output, end with .log ')
parser.add_argument('-i','--input', help='CSV file path contains list of code of works.', required=True)
parser.add_argument('-t','--targetpath', help='Target path contains original files need to be searched.', required=True )
parser.add_argument('-o','--output', help='CSV file with a list of existing files abs paths', required=True)
args = vars(parser.parse_args())

inputCSVPath = args['input']
outputFileListPath = args['output']
targetPath = args['targetpath']

print "输入编号列表：%s" % inputCSVPath
print "输出文件绝对路径列表：%s" % outputFileListPath
print "检测目标文件夹：%s" % targetPath

print "##########################"

if not inputCSVPath or not outputFileListPath or not targetPath:
    print "Input argument Error."

logFilePath = os.path.splitext(outputFileListPath)[0] + '.log'
print "记录文件: %s" % logFilePath
missingFilePath = os.path.splitext(outputFileListPath)[0]+'_missing.csv'
print "丢失文件列表: %s" % missingFilePath

logging.basicConfig(filename=logFilePath, level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始检查文件。')

csvtable = []

outputFileList = []
missingFileList = []





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


loadcsv(inputCSVPath)

for ele in csvtable:
    matches = []
    print "正在查找 %s" % ele[0]
    for root,dirname,filenames in os.walk(targetPath):
        for filename in fnmatch.filter(filenames,ele[0]+'*.*'):
            matches.append(os.path.join(root,filename))
    if not matches:
        #Output to missing list
        missingFileList.append(ele[0])
        outstr = "文件不存在：编号 %s 未找到任何文件。" % ele[0]
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
   
raw_input("按任意键退出")










