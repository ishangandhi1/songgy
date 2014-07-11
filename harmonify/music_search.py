import json
import urllib, urllib2

def music_query(search_terms):
	root_url = 'http://developer.echonest.com/api/v4/'
	source = 'playlist/static'
	search_terms = search_terms.lower()
	search_terms = search_terms.replace(' ','+')
	echo_nest_api = '68NJWFXIG7UDXOTC2'
	search_url = "{0}{1}?api_key={2}&format=json&genre={3}&results=20&type=genre-radio".format(
		root_url,
		source,
		echo_nest_api,
		search_terms)

	results = []
	try:
		response = urllib2.urlopen(search_url).read()
		json_response = json.loads(response)
		#print json_response['response']['songs']
		for song in json_response['response']['songs']:
			results.append({
				'artist':song['artist_name'],
				'title':song['title']
				})

	except urllib2.URLError, e:
		print "Error querying for song", e

	return results