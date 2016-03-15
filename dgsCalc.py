#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import collections


#input data
table = []
#lecture Name List
lectureTable = []
#university list
universityTable = []

markingDict = collections.OrderedDict()
markingDict ={"全国一等奖":10,"全国二等奖":7,"全国三等奖":5,"全国优秀奖":3,"广西一等奖":5,"广西二等奖":3,"广西三等奖":1} 
markingResultIndex = {"全国一等奖":0,"全国二等奖":1,"全国三等奖":2,"全国优秀奖":3,"广西一等奖":4,"广西二等奖":5,"广西三等奖":6} 
markingList = [10,7,5,3,5,3,1]

def loadcsv(filename):
    """
    load prepared csv file
    """
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')      
        for row in csvreader:
            table.append(row)
def writecsv(data, filename, title):
    """
    write output csvfile
    data is a dict
    """
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        if title:
            csvwriter.writerow(title)
        for key,value in data.items():
            
            #value changed, so change output
            if type(value) != type([]):
                #csvwriter.writerow([unicode(key,"utf-8"),value])
                csvwriter.writerow([key,value])
            else:
                #csvwriter doesn't support writing utf-8 in python 2.7.x
                #rowlist = [unicode(key,"utf-8")]
                #value = [s.encode('utf-8') for s in value if type(s) == type('')]
                
                #write as is
                rowlist = [key]
                csvwriter.writerow(rowlist+value)            
                    

def filterLectureName(element):
    """
    filter lecture names.
    input is cell content, return is an array of names
    
    this requires a prepared csv file, all the non-English symbol must be replaced, space must be whitespace, there must not be spaces in name string.
    """
    strTemp = element.strip()
    nameArr = []
    
    #case like:"夏雨　高晓蝉　李珊宇　李杰　杨泽邦"
    #watch out it is not whitespace, but unicode space
    #fix: prepared a changed csv file, removed unicode space
    #bug: if there is a space between charaters for one name, this piece will pick it as two names. TODO:fix this.
    
    if ' ' in strTemp:
        nameArr = strTemp.split(' ')
        nameArr = filter(lambda name: name.strip(), nameArr)      
    #case like:"李娟/梁晨"    
    elif '/' in strTemp:
        nameArr = strTemp.split('/')
        nameArr = filter(lambda name: name.strip(), nameArr)
    #case like only one name:
    else:
        nameArr = [strTemp]
    return nameArr

def getLectureList():
    """
    return a sorted lecture list with marking and work counts
    """
    #start process
    
    #get all the lectures
    #bug: there can be no lecture for one work!
    #TODO: Fix this
    #temporal solution:Just ignore empty lecture ones.
    for row in table:
        namelist = ""
        if row[4].strip() != '':
            namelist += row[4].strip()
        if row[5].strip() != '':
            namelist += ' ' + row[5]
        namelist = filterLectureName(namelist)
        for name in namelist:
            if name not in lectureTable:
                #in case no lecture filled
                if name.strip() != '':
                    lectureTable.append(name)
    #generate mark dict for lecture   
    lectureMark = collections.OrderedDict()
    #[姓名，总分，全国一等奖，全国二等奖，全国三等奖，全国优秀奖，广西一等奖，广西二等奖，广西三等奖，院校,数据检验通过与否,作品总数]
    for name in lectureTable:
        dataArr = [0,0,0,0,0,0,0,0,'',False,0]
        lectureMark[name] = dataArr
        
    #fetch name according to mark
    for row in table:
        
        awardName = row[-1].strip()
        #print awardName

        if awardName in markingDict.keys():
            #get lecture names:
            namelist = ""
            if row[4].strip() != '':
                namelist += row[4].strip()
            if row[5].strip() != '':
                namelist += ' ' + row[5]
            #print namelist
            namelist = filterLectureName(namelist)
            #print namelist
            
            #do not calculate no lecture
            for name in namelist:
                if name.strip() != '':
                    #add mark to lecture
                    lectureMark[name][0] += markingDict[awardName] 
                    #print markingDict[awardName]
                    #get key list
                    keylist = markingDict.keys()
                    #get index in key list
                    index = keylist.index(awardName)
                    lectureMark[name][markingResultIndex[awardName]+1] += 1
                    lectureMark[name][-1] += 1
                    #put university name in data
                    lectureMark[name][-3] = row[6]
        else:
            print "Warning! Anormaly award name detected.!"
            exit(-1)
                
      
    #check if total mark is correct
    for key,value in lectureMark.items():
        if type(value) == type([]):
            #calculating mark
            rowsum = 0
            numsum = 0
            for i in xrange(1,len(value)-3):
                rowsum += value[i] * markingList[i-1]
                numsum += value[i]
            
            #only if total mark and total number matches, then pass
            if rowsum == value[0] and numsum == value[-1]:
                value[-2] = True
            
    #sort ordered dict
    resultDict = collections.OrderedDict(sorted(lectureMark.items(), key = lambda x: x[1][0], reverse = True))

    return resultDict

def getUniversityList():

    universityDict = collections.OrderedDict()
    #row[6] is the university name
    for row in table:
        universityName = row[6].strip()
        if universityName not in universityDict.keys():
            universityDict[universityName] = 1
        else:
            universityDict[universityName] += 1
     
    resultDict = collections.OrderedDict(sorted(universityDict.items(), key = lambda x:x[1], reverse = True))   
    return resultDict
    
if __name__ == "__main__":

    loadcsv('prepared.csv')
    
    if table == []:
        print "Empty table!"
        exit(-1) ;
        
    resultDict = getLectureList()
    #write output lecture list
    title = ["姓名","总分","全国一等奖","全国二等奖","全国三等奖","全国优秀奖","广西一等奖","广西二等奖","广西三等奖","院校","数据检验通过与否","作品总数"]
    writecsv(resultDict,'output.csv',title) 
    
    title = ["院校","作品数"]
    universityResult = getUniversityList()
    writecsv(universityResult, 'university.csv', title)
    
    
        
    
    
