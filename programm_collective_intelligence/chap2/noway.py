import sys
import os
import time
import datetime
import hashlib #import hashlib.md5() as md5()
import http.client 
import urllib, urllib.request, time
from io import StringIO  #真是改的心力交瘁啊哭哭。

#raise except print>> 的写法3里均有改变。
#unichr——chr
__version__ = '0.5.0'
__url__ = 'http://code.google.com/p/pydelicious/'# 这个网址打不开的原因么。因为下面的可以打开的呀。

DLCS_RSS = 'http://del.icio.us/rss/'

USER_AGENT = 'pydelicious.py/%s %s' % (__version__, __url__)


try:
    from elementtree.ElementTree import parse as parse_xml
except ImportError:
    from  xml.etree.ElementTree import parse as parse_xml

class PyDeliciousException(Exception):
    '''Std. pydelicious error'''
    pass

    
import feedparser
def get_popular(tag = ""):
    return getrss(tag = tag, popular = 1)
 
def get_userposts(user):
    return getrss(user = user)

def get_urlposts(url):
    return getrss(url = url)
       
def getrss(tag="", popular=0, url='', user=""):
    
    return dlcs_rss_request(tag=tag, popular=popular, user=user, url=url)
    
    
def dlcs_rss_request(tag = "", popular = 0, user = "", url = ''):
    tag = str2quote(tag)
    user = str2quote(user)
    h=hashlib.md5()
    if url != '':
        url = DLCS_RSS + '''url/%s'''%h.hexdigest()###版本问题咯。
    elif user != '' and tag != '':
        url = DLCS_RSS + '''%(user)s/%(tag)s'''%dict(user=user, tag=tag)
    elif user != '' and tag == '':
        url = DLCS_RSS + '''%s'''%user
    elif popular == 0 and tag == '':
        url = DLCS_RSS
    elif popular == 0 and tag != '':
        url = DLCS_RSS + "tag/%s"%tag
    elif popular == 1 and tag == '':
        url = DLCS_RSS + '''popular/'''
    elif popular == 1 and tag != '':
        url = DLCS_RSS + '''popular/%s'''%tag
    rss = http_request(url).read()
    rss = feedparser.parse(rss)
    l = posts()
    for e in rss.entries:
        if e.has_key("links") and e["links"]!=[] and e["links"][0].has_key("href"):
            url = e["links"][0]["href"]
        elif e.has_key("link"):
            url = e["link"]
        elif e.has_key("id"):
            url = e["id"]
        else:
            url = ""
        if e.has_key("title"):
            description = e['title']
        elif e.has_key("title_detail") and e["title_detail"].has_key("title"):
            description = e["title_detail"]['value']
        else:
            description = ''
        try: tags = e['categories'][0][1]
        except:
            try: tags = e["category"]
            except: tags = ""
        if e.has_key("modified"):
            dt = e['modified']
        else:
            dt = ""
        if e.has_key("summary"):
            extended = e['summary']
        elif e.has_key("summary_detail"):
            e['summary_detail']["value"]
        else:
            extended = ""
        if e.has_key("author"):
            user = e['author']
        else:
            user = ""

        l.append(post(url = url, description = description, tags = tags, dt = dt, extended = extended, user = user))
    return l

def str2quote(s):
    return urllib.parse.quote_plus("".join([chr(ord(i)).encode("utf-8") for i in s]))

   
def http_request(url, user_agent=USER_AGENT, retry=4):
    
    request = urllib.request.Request(url, headers={'User-Agent':user_agent})

    e = None
    tries = retry;
    while tries:
        try:
            return urllib.request.urlopen(request)

        except urllib.error.HTTPError as e: # protocol errors,
            raise PyDeliciousException( "%s" % e)

        except urllib.error.URLError as e:
            print( "%s, %s tries left." % (e, tries),file = sys.stderr,)
            Waiter()
            
            tries = tries - 1
    raise PyDeliciousException ("Unable to retrieve data at '%s', %s" % (url, e))
