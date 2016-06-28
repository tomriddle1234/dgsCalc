# encoding=utf8

# This is a pdf parser that reads informations from DGS pdf forms.

import sys
import pdfquery

reload(sys)
sys.setdefaultencoding('utf8')


pdf = pdfquery.PDFQuery("pdfTest.pdf")
pdf.load()
label = pdf.pq('LTTextLineHorizontal:contains("姓名")')
left_corner = float(label.attr('x0'))
bottom_corner = float(label.attr('y0'))

# bbox value can be measured from Acrobat's measuring tool
name = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner+50, bottom_corner, left_corner+90, bottom_corner+20)).text()

print name
