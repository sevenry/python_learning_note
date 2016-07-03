import akismet
defaultkey = 'yourkeyhere'
pageurl='http:y'
defaultagent='mozilla/5.0(windows;u;windows nt 5.1;en-us;rv:1.8.0.7)'
defaultagent+="gecko/20060909 firefox/1.5.0.7"

def isspam(comment,author,ipaddress,
        agent=defaultagent,
        apikey=defaultkey):
    try:
        valid = akismet.verify_key(apikey,pageurl)
        if valid:
            return akismet.comment_check(apikey,pageurl,
                ipaddress,agent,comment_content=comment,
                comment_author_email=author,comment_type="comment")
        else:
            print("invalid key")
            print False
        except akismet.AkismetError as e:
            print(e.response, e.statuscode)
            return False
        
