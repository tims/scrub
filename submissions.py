import hashlib
import datetime
import urllib,urllib2
import time

user = 'nectarinemango'
passhash = 'be6461e5f3d24c1f916651d366b885a1'
audioscrobbler = 'http://post.audioscrobbler.com/'

def lfmRequest(baseurl, args, data):
    if args:
        url = baseurl + '?' + urllib.urlencode(args)
    else:
        url = baseurl

    #headers = {'host':'last.fm'}
    request = urllib2.Request(url)
    print "Sending request to " + url
    if data:
        request.add_data(urllib.urlencode(data))
        print "With data:"
        print request.get_data()
    
    response = urllib2.urlopen(request)
    status = response.next().strip()
    print status
    if status != 'OK':
        raise Exception('Audioscrobbler message not OK. Got ' + status + '\n' + ''.join(response))
    return response

def handshake(user, passhash):
    timestamp = datetime.datetime.now().strftime('%s')
    md5 = hashlib.md5()
    md5.update(passhash + timestamp)
    token = md5.hexdigest()

    args = {'hs':'true','p':'1.2.1','c':'tst','v':'1.0',\
            'u':user,'t':timestamp,'a':token}
    response = lfmRequest(audioscrobbler, args, None)
    sessionid = response.next().strip()
    nowplayingUrl = response.next().strip()
    submissionsUrl = response.next().strip()
    return sessionid, nowplayingUrl, submissionsUrl

""" tracknumber = track position on album
    mbid = music brainz id
"""
def nowplaying(url, sessionid, artist, track, album='', length='', tracknumber='', mbid=''):
    data = {'s':sessionid, 'a':artist, 't':track, 'b':album, 'l':length, 'n':tracknumber,'m':mbid}
    lfmRequest(url, None, data)

def submission(url, sessionid, artist, track, time, source, rating='', length='', album='', tracknumber='', mbid=''):
    i = 0
    data = {'s':sessionid, 'a[%s]'%i:artist, 't[%s]'%i:track, 'i[%s]'%i:time, 'o[%s]'%i:source,
            'r[%s]'%i:rating, 'l[%s]'%i:length, 'b[%s]'%i:album, 'n[%s]'%i:tracknumber,'m[%s]'%i:mbid}
    lfmRequest(url, None, data)

success = False
tries = 0
while not success and tries < 1:
    try:
        tries += 1
        print 'Handshaking for user ' + user
        sessionid, nowplayingUrl, submissionsUrl = handshake(user, passhash)
        print 'Session ID = ' + sessionid

        artist = 'Test Artist'
        track = 'Hmm 2'

        print 'Sending now playing info'
        #nowplaying(nowplayingUrl, sessionid, artist, track, length='30')
        print 'done.'

        #time.sleep()
        listentime = datetime.datetime.now().strftime('%s')
        print 'Submitting track'
        submission(submissionsUrl, sessionid, artist, track, listentime, 'P', length='30')
        print 'done.'
        success = True
    except Exception, e:
        print e
        success = False
    

