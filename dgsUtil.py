# encoding=utf8

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
