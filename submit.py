#!/usr/bin/python
import submissions, auth
import datetime
import sys
import yaml

def getScrobbleSession(sessionsFile, user, password, timestamp, authToken):
    sessionsFile = 'sessions.yaml'
    sessions = {}
    try:
        f = open(sessionsFile, 'r')
        sessions = yaml.load(f)
        f.close()
    except:
        print "Couldn't open sessions.yaml will authorize from scratch\n"
    if not sessions: sessions = {}

    wsSessions = sessions.get('ws', {})
    scrobbleSessions = sessions.get('scrobble',{})

    if user in scrobbleSessions:
        scrobbleSession, nowplayingUrl, submissionsUrl = scrobbleSessions[user]
        print "Using existing scrobble session:", scrobbleSession
    else:
        if user in wsSessions:
            wsSession = wsSessions[user]
            print "Using existing webservice session:", wsSession
        else:
            print "Authorizing via webservice api..."
            wsSession = auth.getMobileSession(user,password)
            wsSessions[user] = str(wsSession)
        scrobbleSession, nowplayingUrl, submissionsUrl = submissions.handshake(user, timestamp, authToken, apiKey=auth.apiKey, sessionKey=wsSession)
        scrobbleSessions[str(user)] = [str(scrobbleSession), str(nowplayingUrl), str(submissionsUrl)]
    sessions = {'ws':wsSessions, 'scrobble':scrobbleSessions}
    f = open(sessionsFile,'w')
    yaml.dump(sessions, f)
    f.close()
    return scrobbleSession, nowplayingUrl, submissionsUrl

def main(args):
    sessionsFile = 'sessions.yaml'

    user = args[0]
    password = args[1]
    artist = args[2]
    track = args[3]

    print 'Using:'
    print 'User: ' + user
    print 'Password: ' + password
    print 'Artist: ' + artist
    print 'Track: ' + track

    timestamp = datetime.datetime.now().strftime('%s')
    authToken = auth.md5(auth.apiSecret + timestamp)

    scrobbleSession, nowplayingUrl, submissionsUrl = getScrobbleSession(sessionsFile, user, password, timestamp, authToken)
    submissions.submission(submissionsUrl, scrobbleSession, artist, track, timestamp, 'P', rating='', length='30', album='', tracknumber='', mbid='')

def usage():
    usage = \
    """Usage:
    submit.py <user> <password> <artist> <track>"""
    print usage


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 4:
        usage()
        sys.exit()
    main(args)



