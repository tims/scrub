import hashlib
import datetime
import urllib,urllib2
import time

user = 'nectarinemango'
passhash = 'be6461e5f3d24c1f916651d366b885a1'
audioscrobbler = 'http://post.audioscrobbler.com/'

def submRequest(baseurl, args, data):
    if args:
        url = baseurl + '?' + urllib.urlencode(args)
    else:
        url = baseurl

    request = urllib2.Request(url)
    print "Sending request to " + url
    if data:
        request.add_data(urllib.urlencode(data))
        print "With data:", data
    
    try:
        response = urllib2.urlopen(request)
    except HTTPError, e:
        raise Exception('Webservice call not ok. Got:\n' +''.join(e))

    response = urllib2.urlopen(request)
    status = response.next().strip()
    print status
    if status != 'OK':
        raise Exception('Audioscrobbler message not OK. Got ' + status + '\n' + ''.join(response))
    return response

def handshake(user, timestamp, token, apiKey='', sessionKey='', protocol='1.2.1', client='tst', version='1.0'):
    args = {'hs':'true','p':protocol,'c':client,'v':version,\
            'u':user,'t':timestamp,'a':token, 'api_key':apiKey, 'sk':sessionKey}
    response = submRequest(audioscrobbler, args, None)
    sessionid = response.next().strip()
    nowplayingUrl = response.next().strip()
    submissionsUrl = response.next().strip()
    return sessionid, nowplayingUrl, submissionsUrl

""" tracknumber = track position on album
    mbid = music brainz id
"""
def nowplaying(url, sessionid, artist, track, album='', length='', tracknumber='', mbid=''):
    data = {'s':sessionid, 'a':artist, 't':track, 'b':album, 'l':length, 'n':tracknumber,'m':mbid}
    submRequest(url, None, data)

def submission(url, sessionid, artist, track, time, source, rating='', length='', album='', tracknumber='', mbid=''):
    i = 0
    data = {'s':sessionid, 'a[%s]'%i:artist, 't[%s]'%i:track, 'i[%s]'%i:time, 'o[%s]'%i:source,
            'r[%s]'%i:rating, 'l[%s]'%i:length, 'b[%s]'%i:album, 'n[%s]'%i:tracknumber,'m[%s]'%i:mbid}
    submRequest(url, None, data)

