####sss666

read_csv 177

sys.stdout###np.sys.stdout

to_csv(cols)##columns

分隔符 182页  不太懂哎哎。
class 那一段。

web信息也迷迷糊糊。（主要是无法删除空格）

from lxml.html import parse
from urllib.request import urlopen
parsed=parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))
doc=parsed.getroot()
tables=doc.findall('.//table')
#print(tables)
rows=[]
for i in range(len(tables)):
    rows.append(tables[i].findall('.//tr'))
    #print(rows[i],'\n')
    
def _unpack(row,kind='td'):
    elts=row.findall('.//%s' %kind)
    return [val.text_content() for val in elts]
    
    
#print(_unpack(rows[2][1],kind='td'))##

for i in range(len(rows)):
    print(_unpack(rows[i][0],kind='th'))###这一行需要解决的是消除空格什么的。
    if len(rows[i])>1:
        print(_unpack(rows[i][1],kind='td'))###为啥不能print，没有print是可以的呀。
#189页。dataframe没有save项。

###191页。无论如何data=json.loads(resp.text)都有问题。

###194页 zip不懂哎。181页也是。
#并且194页。sql行并没有read_frame 这个方法，我用read_sql也可以啊。
#最后MongoDB 并没有看。