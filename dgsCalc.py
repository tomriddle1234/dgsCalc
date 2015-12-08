#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

#load csv

table = []
lectureTable = []

markingDict = dict()
markingDict ={"全国一等奖":10,"全国二等奖":7,"全国三等奖":5,"全国优秀奖":3,"广西一等奖":5,"广西二等奖":3,"广西三等奖":1} 

def loadcsv(filename):
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')      
        for row in csvreader:
            table.append(row)
def writecsv(data, filename):
    """
    data is a dict
    """
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        for key,value in data.items():
            csvwriter.writerow([key,value])

def filterLectureName(element):
    """
    input is cell containt, return is an array of names
    
    this requires a prepared csv file, all the non-English symbol must be replaced, space must be whitespace, there must not be spaces in name string.
    """
    strTemp = element.strip()
    nameArr = []
    
    #case like:"夏雨　高晓蝉　李珊宇　李杰　杨泽邦"
    #watch out it is not whitespace, but unicode space
    #fix: prepared a changed csv file, removed unicode space
    if ' ' in strTemp:
        nameArr = strTemp.split(' ')
        nameArr = filter(lambda name: name.strip(), nameArr)      
    #case like:"李娟/梁晨"    
    elif '/' in strTemp:
        nameArr = strTemp.split('/')
        nameArr = filter(lambda name: name.strip(), nameArr)
    return nameArr
    
if __name__ == "__main__":

    loadcsv('prepared.csv')
    
    if table == []:
        print "Empty table!"
        exit(-1) ;
    #start process
    
    #get all the lectures
    for row in table:
        namelist = ""
        namelist += row[4]
        namelist += ' ' + row[5]
        namelist = filterLectureName(namelist)
        
        for name in namelist:
            if name not in lectureTable:
                lectureTable.append(name)
    #generate mark dict for lecture   
    lectureMark = dict()
    for name in lectureTable:
        lectureMark[name] = 0
        
    #fetch name according to mark
    for row in table:
        
        awardName = row[-1].strip()
        if awardName in markingDict.keys():
            #get lecture names:
            namelist = ""
            namelist += row[4]
            namelist += ' ' + row[5]
            namelist = filterLectureName(namelist)
            for name in namelist:
                #add mark to lecture
                lectureMark[name] += markingDict[awardName] 
    
    #sort marking dict and save csv
    #no need to sort
    writecsv(lectureMark,'output.csv') 
    
    
        
    
    
