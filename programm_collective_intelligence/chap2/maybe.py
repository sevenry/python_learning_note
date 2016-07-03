
import sys
import os
import time
import datetime
import hashlib #import hashlib.md5() as md5
import http.client 
import urllib, urllib.request, time
from io import StringIO  #真是改的心力交瘁啊哭哭。
#我确实是没办法拯救了。现在的报错信息都在安装包里……
try:
    from elementtree.ElementTree import parse as parse_xml
except ImportError:
    from  xml.etree.ElementTree import parse as parse_xml

import feedparser


### Static config

__version__ = '0.5.0'
__author__ = 'Frank Timmermann <regenkind_at_gmx_dot_de>' # GP: does not respond to emails
__contributors__ = [
    'Greg Pinero',
    'Berend van Berkum <berend+pydelicious@dotmpe.com>']
__url__ = 'http://code.google.com/p/pydelicious/'
__author_email__ = ""
# Old URL: 'http://deliciouspython.python-hosting.com/'

__description__ = '''pydelicious.py allows you to access the web service of del.icio.us via it's API through python.'''
__long_description__ = '''the goal is to design an easy to use and fully functional python interface to del.icio.us. '''

DLCS_OK_MESSAGES = ('done', 'ok') # Known text values of positive del.icio.us <result> answers
DLCS_WAIT_TIME = 4
DLCS_REQUEST_TIMEOUT = 444 # Seconds before socket triggers timeout
#DLCS_API_REALM = 'del.icio.us API'
DLCS_API_HOST = 'https://api.del.icio.us'
DLCS_API_PATH = 'v1'
DLCS_API = "%s/%s" % (DLCS_API_HOST, DLCS_API_PATH)
DLCS_RSS = 'http://del.icio.us/rss/'

ISO_8601_DATETIME = '%Y-%m-%dT%H:%M:%SZ'

USER_AGENT = 'pydelicious.py/%s %s' % (__version__, __url__)

DEBUG = 0
if 'DLCS_DEBUG' in os.environ:
    DEBUG = int(os.environ['DLCS_DEBUG'])


try:
    import timeoutsocket # http://www.timo-tasi.org/python/timeoutsocket.py
    timeoutsocket.setDefaultSocketTimeout(DLCS_REQUEST_TIMEOUT)
except ImportError:
    import socket
    if hasattr(socket, 'setdefaulttimeout'): socket.setdefaulttimeout(DLCS_REQUEST_TIMEOUT)
if DEBUG: print >>sys.stderr, "Set socket timeout to %s seconds" % DLCS_REQUEST_TIMEOUT


### Utility classes

class _Waiter:
    
    def __init__(self, wait):
        self.wait = wait
        self.waited = 0
        self.lastcall = 0;

    def __call__(self):
        tt = time.time()

        timeago = tt - self.lastcall

        if self.lastcall and DEBUG>2:
            print >>sys.stderr, "Lastcall: %s seconds ago." % lastcall

        if timeago <= self.wait:
            if DEBUG>0: print >>sys.stderr, "Waiting %s seconds." % self.wait
            time.sleep(self.wait)
            self.waited += 1
            self.lastcall = tt + self.wait
        else:
            self.lastcall = tt

Waiter = _Waiter(DLCS_WAIT_TIME)

class PyDeliciousException(Exception):
    '''Std. pydelicious error'''
    pass

class DeliciousError(Exception):
    '''nothing'''

	
class DefaultErrorHandler(urllib.request.HTTPDefaultErrorHandler):
    
    def http_error_503(self, req, fp, code, msg, headers):
        raise urllib.request.HTTPError(req, code, throttled_message, headers, fp)


class post(dict):
   
    def __init__(self, href = "", description = "", hash = "", time = "", tag = "", extended = "", user = "", count = "",
                 tags = "", url = "", dt = ""): # tags or tag?
        self["href"] = href
        if url != "": self["href"] = url
        self["description"] = description
        self["hash"] = hash
        self["dt"] = dt
        if time != "": self["dt"] = time
        self["tags"] = tags
        if tag != "":  self["tags"] = tag     # tag or tags? # !! tags
        self["extended"] = extended
        self["user"] = user
        self["count"] = count

    def __getattr__(self, name):
        try: return self[name]
        except: object.__getattribute__(self, name)


class posts(list):
    
    def __init__(self, *args):
        for i in args: self.append(i)

    def __getattr__(self, attr):
        try: return [p[attr] for p in self]
        except: object.__getattribute__(self, attr)


def str2uni(s):
    return ("".join([chr(ord(i)) for i in s]))

def str2utf8(s):
    kk=[chr(ord(i)).encode("utf-8") for i in s]
    return ("".join([str(item) for item in kk]))# join写法也有变化。

def str2quote(s):
    kk=[chr(ord(i)).encode("utf-8") for i in s]
    return urllib.parse.quote_plus("".join([str(item) for item in kk]))

def dict0(d):
    dd = dict()
    for i in d:
            if d[i] != "": dd[i] = d[i]
    return dd

def delicious_datetime(str):
    return datetime.datetime(*time.strptime(str, ISO_8601_DATETIME)[0:6])

   
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



def http_auth_request(url, host, user, passwd, user_agent=USER_AGENT):
    if DEBUG: httplib.HTTPConnection.debuglevel = 1
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, host, user, passwd)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)

    return http_request(url, user_agent)

def dlcs_api_request(path, params='', user='', passwd='', throttle=True):
    if throttle:
        Waiter()

    if params:
        # params come as a dict, strip empty entries and urlencode
        url = "%s/%s?%s" % (DLCS_API, path, urllib.urlencode(dict0(params)))
    else:
        url = "%s/%s" % (DLCS_API, path)

    if DEBUG: print ("dlcs_api_request: %s" % url, file = sys.stderr)

    try:
        return http_auth_request(url, DLCS_API_HOST, user, passwd, USER_AGENT)

    # @bvb: Is this ever raised? When?
    except DefaultErrorHandler as e:
        print ( "%s" % e, file=sys.stderr)

def dlcs_parse_xml(data, split_tags=False):

    if DEBUG>3: print ("dlcs_parse_xml: parsing from ", data, file=sys.stderr)

    if not hasattr(data, 'read'):
        data = StringIO(data)

    doc = parse_xml(data)
    root = doc.getroot()
    fmt = root.tag

	# Split up into three cases: Data, Result or Update
    if fmt in ('tags', 'posts', 'dates', 'bundles'):
        elist = [el.attrib for el in doc.findall(fmt[:-1])]
        data = {fmt: elist}

        data.update(root.attrib)

        return data

    elif fmt == 'result':

        if root.attrib.has_key('code'):
            msg = root.attrib['code']
        else:
            msg = root.text

        v = msg in DLCS_OK_MESSAGES
        return {fmt: (v, msg)}

    elif fmt == 'update':
        return {fmt: {'time':time.strptime(root.attrib['time'], ISO_8601_DATETIME)}}

    else:
        raise PyDeliciousException ( "Unknown XML document format '%s'" % fmt)
 
def dlcs_rss_request(tag = "", popular = 0, user = "", url = ''):
    tag = str2quote(tag)
    user = str2quote(user)
    if url != '':
        # http://del.icio.us/rss/url/efbfb246d886393d48065551434dab54
        #url = DLCS_RSS + '''url/%s'''%md5.new(url).hexdigest()
        h=hashlib.md5()
        url = DLCS_RSS + '''url/%s'''%h.hexdigest()###版本问题咯。
    
    elif user != '' and tag != '':
        url = DLCS_RSS + '''%(user)s/%(tag)s'''%dict(user=user, tag=tag)
    elif user != '' and tag == '':
        # http://del.icio.us/rss/delpy
        url = DLCS_RSS + '''%s'''%user
    elif popular == 0 and tag == '':
        url = DLCS_RSS
    elif popular == 0 and tag != '':
        # http://del.icio.us/rss/tag/apple
        # http://del.icio.us/rss/tag/web2.0
        url = DLCS_RSS + "tag/%s"%tag
    elif popular == 1 and tag == '':
        url = DLCS_RSS + '''popular/'''
    elif popular == 1 and tag != '':
        url = DLCS_RSS + '''popular/%s'''%tag
    rss = http_request(url).read()
    rss = feedparser.parse(rss)
    # print rss
#     for e in rss.entries: print e;print
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
#  time = dt ist weist auf ein problem hin
# die benennung der variablen ist nicht einheitlich
#  api senden und
#  xml bekommen sind zwei verschiedene schuhe :(
        l.append(post(url = url, description = description, tags = tags, dt = dt, extended = extended, user = user))
    return l


### Main module class

class DeliciousAPI:

    def __init__(self, user, passwd, codec='iso-8859-1', api_request=dlcs_api_request, xml_parser=dlcs_parse_xml):
        assert user != ""
        self.user = user
        self.passwd = passwd
        self.codec = codec

        assert callable(api_request)
        self._api_request = api_request
        assert callable(xml_parser)
        self._parse_response = xml_parser

    def _call_server(self, path, **params):
        params = dict0(params)
        for key in params:
            params[key] = params[key].encode(self.codec)

        return self._api_request(path, params, self.user, self.passwd)
        
    def request(self, path, _raw=False, **params):
        if _raw:
            # return answer
            return self.request_raw(path, **params)

        else:
            # get answer and parse
            fl = self._call_server(path, **params)
            rs = self._parse_response(fl)

			# Raise an error for negative 'result' answers
            if type(rs) == dict and rs == 'result' and not rs['result'][0]:
                errmsg = ""
                if len(rs['result'])>0:
                    errmsg = rs['result'][1:]
                raise DeliciousError (errmsg)

            return rs

    def request_raw(self, path, **params):
        return self._call_server(path, **params)

    def tags_get(self, **kwds):
        return self.request("tags/get", **kwds)

    def tags_rename(self, old, new, **kwds):
        return self.request("tags/rename", old=old, new=new, **kwds)

    # Posts
    def posts_update(self, **kwds):
        return self.request("posts/update", **kwds)

    def posts_dates(self, tag="", **kwds):
        return self.request("posts/dates", tag=tag, **kwds)

    def posts_get(self, tag="", dt="", url="", **kwds):
        
        return self.request("posts/get", tag=tag, dt=dt, url=url, **kwds)

    def posts_recent(self, tag="", count="", **kwds):
       
        return self.request("posts/recent", tag=tag, count=count, **kwds)

    def posts_all(self, tag="", **kwds):
       
        return self.request("posts/all", tag=tag, **kwds)

    def posts_add(self, url, description, extended="", tags="", dt="",
            replace="no", shared="yes", **kwds):
       
        return self.request("posts/add", url=url, description=description,
                extended=extended, tags=tags, dt=dt,
                replace=replace, shared=shared, **kwds)

    def posts_delete(self, url, **kwds):
       
        return self.request("posts/delete", url=url, **kwds)

    # Bundles
    def bundles_all(self, **kwds):
        return self.request("tags/bundles/all", **kwds)

    def bundles_set(self, bundle, tags, **kwds):
       
        if type(tags)==list:
            tags = " ".join(tags)
        return self.request("tags/bundles/set", bundle=bundle, tags=tags,
                **kwds)

    def bundles_delete(self, bundle, **kwds):

        return self.request("tags/bundles/delete", bundle=bundle, **kwds)

    ### Utils

    # Lookup table for del.icio.us url-path to DeliciousAPI method.
    paths = {
        'tags/get': tags_get,
        'tags/rename': tags_rename,
        'posts/update': posts_update,
        'posts/dates': posts_dates,
        'posts/get': posts_get,
        'posts/recent': posts_recent,
        'posts/all': posts_all,
        'posts/add': posts_add,
        'posts/delete': posts_delete,
        'tags/bundles/all': bundles_all,
        'tags/bundles/set': bundles_set,
        'tags/bundles/delete': bundles_delete,
    }

    def get_url(self, url):
        """Return the del.icio.us url at which the HTML page with posts for
        ``url`` can be found.
        """
        return "http://del.icio.us/url/?url=%s" % (url,)


### Convenience functions on this package

def apiNew(user, passwd):
    """creates a new DeliciousAPI object.
    requires user(name) and passwd
	"""
    return DeliciousAPI(user=user, passwd=passwd)

def add(user, passwd, url, description, tags="", extended="", dt="", replace="no"):
    return apiNew(user, passwd).posts_add(url=url, description=description, extended=extended, tags=tags, dt=dt, replace=replace)

def get(user, passwd, tag="", dt="",  count = 0):
    posts = apiNew(user, passwd).posts_get(tag=tag,dt=dt)
    if count != 0: posts = posts[0:count]
    return posts

def get_all(user, passwd, tag=""):
    return apiNew(user, passwd).posts_all(tag=tag)

def delete(user, passwd, url):
    return apiNew(user, passwd).posts_delete(url=url)

def rename_tag(user, passwd, oldtag, newtag):
    return apiNew(user=user, passwd=passwd).tags_rename(old=oldtag, new=newtag)

def get_tags(user, passwd):
    return apiNew(user=user, passwd=passwd).tags_get()

def getrss(tag="", popular=0, url='', user=""):
    
    return dlcs_rss_request(tag=tag, popular=popular, user=user, url=url)

def get_userposts(user):
    return getrss(user = user)

def get_tagposts(tag):
    return getrss(tag = tag)

def get_urlposts(url):
    return getrss(url = url)

def get_popular(tag = ""):
    return getrss(tag = tag, popular = 1)

def json_posts(user, count=15):
    '''bbb'''

def json_tags(user, atleast, count, sort='alpha'):
    '''bbb'''

def json_network(user):
    '''bbb'''
    

def json_fans(user):
    '''bbb'''
   