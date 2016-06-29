# encoding=utf8
import csv
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
    data is a list
    """
    with open(filename,'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        if title:
            csvwriter.writerow(title)
        for value in data:
            csvwriter.writerow([value])

def gbk2utf8(src):
    if isinstance(src,unicode):
	    return src
    else:
	    return src.decode('gb2312').encode('utf-8')
	    
def utf82gbk(src):
    if isinstance(src,unicode):
        return src.decode('utf-8').encode('gb2312')
    else:
        return src
