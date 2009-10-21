import urllib, urllib2
from urllib2 import HTTPError
import hashlib
from BeautifulSoup import BeautifulStoneSoup
import os

apiKey = '8fdab086c81a5bd9df3c1c4c46796ae0'
apiSecret = '195924675c89d2da66d230292080753a'
webservices = 'http://ws.audioscrobbler.com/2.0/'

def md5(word):
    md5 = hashlib.md5()
    md5.update(word)
    return md5.hexdigest()

def getUrl(baseurl, params):
    if params:
        items = params.items()
        items.sort()
        url = baseurl + '?' + urllib.urlencode(items)
    else:
        url = baseurl
    return url

def wsRequest(params):
    url = getUrl(webservices, params)

    request = urllib2.Request(url)
    print "Sending request to " + url
    
    try:
        response = urllib2.urlopen(request)
    except HTTPError, e:
        soup = BeautifulStoneSoup(e)
        raise Exception('Webservice call not ok. Got:\n' +soup.prettify())

    soup = BeautifulStoneSoup(response)
    #print soup.prettify()
    #status = soup.lfm.get('status')
    return soup.lfm

def sign(params):
    items = params.items()
    items.sort()
    methodSig = ''
    for k,v in items:
        methodSig += k + v
    return md5(methodSig + apiSecret)

def getToken():
    method = 'auth.getToken'
    params = {'method': method, 'api_key': apiKey}
    response = wsRequest(params)
    token = response.token.string
    return token

def authorizeToken(token):
    url = getUrl('http://www.last.fm/api/auth/', {'api_key': apiKey, 'token': token})
    print url
    os.system('firefox "'+ url + '"')

def getSession(token):
    method = 'auth.getSession'
    params = {'method':method, 'api_key': apiKey, 'token':token}
    params['api_sig'] = sign(params)
    response = wsRequest(params)
    session = response.session.key.string
    return session
    
def getMobileSession(username, password):
    authToken = md5(username + md5(password))
    method = 'auth.getMobileSession'
    params = {'method':method,'username':username, 'authToken':authToken, 'api_key': apiKey}
    params['api_sig'] = sign(params)
    response = wsRequest(params)
    session = response.session.key.string
    return session


