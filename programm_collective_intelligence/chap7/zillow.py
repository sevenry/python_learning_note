import xml.dom.minidom
import urllib.request

zwskey="X1-ZWz1chwxis15aj_9skq6"

def getaddressdata(address,city):
  escad=address.replace(' ','+')
  print(escad)
  url='http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
  url+='zws-id=%s&address=%s&citystatezip=%s' % (zwskey,escad,city)
  doc=xml.dom.minidom.parseString(urllib.request.urlopen(url).read())
  code=doc.getElementsByTagName('code')[0].firstChild.data
  ###print(code)#####why not 0?????
  if code!='0': return None
  if 1:
    zipcode=doc.getElementsByTagName('zipcode')[0].firstChild.data
    use=doc.getElementsByTagName('useCode')[0].firstChild.data
    print(use)
    year=doc.getElementsByTagName('yearBuilt')[0].firstChild.data
    sqft=doc.getElementsByTagName('finishedSqFt')[0].firstChild.data
    bath=doc.getElementsByTagName('bathrooms')[0].firstChild.data
    bed=doc.getElementsByTagName('bedrooms')[0].firstChild.data
    rooms=1 #doc.getElementsByTagName('totalRooms')[0].firstChild.data
    price=doc.getElementsByTagName('amount')[0].firstChild.data
  else:
    return None
  
  return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)
  #return (zipcode,use,float(bath),int(bed),int(rooms),price)


def getpricelist():
  l1=[]
  for line in open('addresslist.txt'):
    data=getaddressdata(line.strip(),'Pearl')
    l1.append(data)
  return l1