import feedparser
import re
import docclass
def read(feed,classifier):
  f=feedparser.parse(feed)
 
  for entry in f['entries']:
    #print(entry)
    
    print ()#这一行在干嘛
    print('-----') 
    #print('title')
    #print(entry['title'].encode('utf-8'))
    print ('Title:     ',entry['title'].encode('utf-8'))
    print ('Publisher: ',entry['publisher'].encode('utf-8'))
    print ()
    print (entry['summary'].encode('utf-8'))
    '''
    print ('Title:     '+entry['title'].encode('utf-8'))
    print ('Publisher: '+entry['publisher'].encode('utf-8'))
    print ()
    print (entry['summary'].encode('utf-8'))
    '''

    #fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])
    #print(fulltext)
    #aaa=str(classifier.classify(fulltext))
    #print(aaa)
    #print ('Guess: '+str(classifier.classify(fulltext)))
    print ('Guess: '+str(classifier.classify(entry)))

    c1=input('Enter category: ')
   
    #print('hhh',entry)
    #print(c1)
    #classifier.train(fulltext,c1)
    classifier.train(entry,c1)

def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  
  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1
    
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
    
  f['Publisher:'+entry['publisher']]=1

  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  
  return f


