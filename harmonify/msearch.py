import json
import urllib, urllib2


def genre_query(artist_id):
	root_url = 'http://developer.echonest.com/api/v4/'
	source = 'artist/profile'
	#search_terms = search_terms.replace(' ','+')
	echo_nest_api = '68NJWFXIG7UDXOTC2'
	search_url = "{0}{1}?api_key={2}&id={3}&format=json&bucket=genre".format(
		root_url,
		source,
		echo_nest_api,
		artist_id)

	all_genres = []
	try:
		response = urllib2.urlopen(search_url).read()
		json_response = json.loads(response)
		#print json_response['response']['songs']
		for genre in json_response['response']['artist']['genres']:

			all_genres.append(genre['name'])

		tmp = " ".join(x for x in all_genres)
		tmp_l = tmp.split();
		from collections import defaultdict
		import re
		d = defaultdict(int)
		for x in tmp_l:
			d[x]+=1
		r = max(d.iteritems(),key=lambda x: x[1])
		results = r[0]	

	except urllib2.URLError, e:
		print "Error querying for genre", e

	return results