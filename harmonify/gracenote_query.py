import sys, pygn, json, pickle


clientID = '5245952-BD676412A035BCA19C8120F75D2082CA' # Enter your Client ID from developer.gracenote.com here
#userID = pygn.register(clientID) # Get a User ID from pygn.register() - Only register once per end-user

#with open('uid.pkl', 'wb') as output:
#    pickle.dump(userID, output, pickle.HIGHEST_PROTOCOL)

with open('uid.pkl', 'rb') as input:
    userID = pickle.load(input)         


"""
print '\nSearch for artist "Kings of Convenience"\n'
result = pygn.search(clientID=clientID, userID=userID, artist='Kings of Convenience')
print json.dumps(result, sort_keys=True, indent=4)

print '\nSearch for album "Prism" by "Katy Perry"\n'
result = pygn.search(clientID=clientID, userID=userID, artist='Katy Perry', album='Prism')
print json.dumps(result, sort_keys=True, indent=4)

print '\nSearch for track "Drop" by "Cornelius"\n'
result = pygn.search(clientID=clientID, userID=userID, artist='OneRepublic', track='Marchin On')
print json.dumps(result, sort_keys=True, indent=4)


print '\nGetting artist discography for "Daft Punk"\n'
result = pygn.get_discography(clientID=clientID, userID=userID, artist='Daft Punk')
print json.dumps(result, sort_keys=True, indent=4)
"""

def get_gracenote_genre(artist='', track=''):
	result = pygn.search(clientID=clientID, userID=userID, artist=artist, track=track)
	#print json.dumps(result, sort_keys=True, indent=4)
	return result['genre']['1']['TEXT']
