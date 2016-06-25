# encoding=utf8

import sys,os
import logging

from openpyxl import load_workbook

reload(sys)
sys.setdefaultencoding('utf8')

categoryList = ["平面类","视频类","动画类","互动类","广播类","策划案类","营销创客类","公益类"]

xlFilename = 'prepared2.xlsx'

### Logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('开始机检。%s' % xlFilename)

#if read only there will be bugs on loading cell values
wb = load_workbook(xlFilename)

sheetNameList = wb.get_sheet_names()

ws = wb.worksheets[0]


def utilGetTotalRecords(ws):
    row_count = ws.max_row
    column_count = ws.max_column
    valid_count = 0
    result = 0
    for i in range(3,row_count):     
        if  ws.cell(row=i,column=1).value is None or ws.cell(row=i,column=1).value == "汇总":
            break
        result += 1
     
#    for i in range(3,row_count):     
#        if  ws.cell(row=i,column=3).value.strip() == "作品数合计：":
#            given = int(ws.cell(row=i,column=4).value)
#            if given != result:
#                outstr = "机检作品数合计 %d 与表格给出数据 %d 不符，检查第 %d 排第4列。" % (result,given,i)
#                print outstr
#                logging.warning(outstr)
                     
    return result

recordsCount = utilGetTotalRecords(ws)

def utilCheckIfAllChinese(input_str):
    """
        Reuqire input is a utf8 string.
    """
    if not all((u'\u4e00' <= c <= u'\u9fff') or (c == ',') or (c == u'，') for c in input_str.decode('utf-8')):
        return False
    return True

def utilCheckIfCellEmpty(input_cell,s,i):
    if input_cell.value is None:
        outstr = "第 %d 排 %s 是空白的。" % (i, s)
        print outstr
        logging.warning(outstr)
        
     
    

def checkCategoryName(ws):
    """
    Function : Check if category name is in given list of strings
    """
    row_count = ws.max_row
    column_count = ws.max_column
    
    result = True
    for i in range(3,3+recordsCount):     
        utilCheckIfCellEmpty(ws.cell(row=i,column=2),"命题类别",i)
        # if there is a category name not in the list log this
        if not ws.cell(row=i,column=2).value.strip() in categoryList:
            outstr = "命题类别第 %s 排,第 %s 列不在类别名称列表中。" % (str(i),'2')
            print outstr
            logging.warning(outstr)
            result = False
    return result 


def checkTeamMemberNames(ws):
    """
    Function : Check if team member and teacher's names in right format
    """
    row_count = ws.max_row
    column_count = ws.max_column
    
    result = True
    for i in range(3,3+recordsCount):     
        utilCheckIfCellEmpty(ws.cell(row=i,column=7),"作者",i)
        # if name contains spaces
        if (' ' in ws.cell(row=i,column=7).value) or ('　' in ws.cell(row=i,column=7).value):
            outstr = "第 %d　排作者名称中出现空格。" % i
            print outstr
            logging.warning(outstr)
            result = False
        elif '、' in ws.cell(row=i,column=7).value:
            outstr = "第 %d　排作者名称中出现顿号。" % i
            print outstr
            logging.warning(outstr)
            result = False
        elif not utilCheckIfAllChinese(ws.cell(row=i,column=7).value):
            outstr = "第 %d　排指导教师名称中出现其它特殊符号。" % i
            print outstr
            logging.warning(outstr)
            result = False
    return result 

def checkTeacherMemberNames(ws):
    """
    Function : Check if team member and teacher's names in right format
    """
    row_count = ws.max_row
    column_count = ws.max_column
    
    result = True
    for i in range(3,3+recordsCount):     
        utilCheckIfCellEmpty(ws.cell(row=i,column=9),"指导教师",i)
        # if name contains spaces
        
        if (u'\x20' in ws.cell(row=i,column=9).value) or (u'\u3000' in ws.cell(row=i,column=9).value):
            outstr = "第 %d　排指导教师名称中出现空格。" % i
            print outstr
            logging.warning(outstr)
            result = False
        elif  '、' in ws.cell(row=i,column=9).value:
            outstr = "第 %d　排指导教师名称中出现顿号。" % i
            print outstr
            logging.warning(outstr)
            result = False  
        elif not utilCheckIfAllChinese(ws.cell(row=i,column=9).value):
            outstr = "第 %d　排指导教师名称中出现其它特殊符号。" % i
            print outstr
            logging.warning(outstr)
            result = False
    return result 


def checkNewFormat(ws):
    """
    Function : Check if this table is the new format or the old format
    
    Check new or old by the second row
    """
    row_count = ws.max_row
    column_count = ws.max_column
    rowelements = []
    result = True
    for i in range(1,column_count):
        rowelements.append(ws.cell(row=2,column=i).value)
    
    for ele in rowelements:
        if "师2" in ele:
            result = False
            break
    
    if "系列件数" not in rowelements:
        result = False
    
    if not result:
        outstr = ">>>此表格是旧表。<<<"
    else:
        outstr = ">>>此表格是新表。<<<"

    print outstr
    logging.warning(outstr)
    
    
    
    
    
    
        
    
    
    
    
#Test

checkNewFormat(ws)

checkCategoryName(ws)

checkTeamMemberNames(ws)

checkTeacherMemberNames(ws)

logging.info('机检完毕。%s' % xlFilename)



#print ws['A2'].value.encode('utf8')

#print ws.cell(row=3,column=2).value


#Function : Check if work category is following order. 

#Function : Check if work encoded number is in right format







#Function : Check if the work total numbers are calculated right



#Function : Check if work encoded number is following order.

#Function : Label wrong records or cells with related color

#Function : Generate a log and report file.

#Function : Generate a statistic table and compare it with the given statistics


