from __future__ import print_function
import collections

"""Example script that identifies metadata for files specified on the
command line.
"""
import acoustid
import sys

# API key for this demo script only. Get your own API key at the
# Acoustid Web for your application.
# http://acoustid.org/
API_KEY = 'YmIDkujU'

def aidmatch(filename):
    try:
        results = acoustid.match(API_KEY, filename)
    except acoustid.NoBackendError:
        print("chromaprint library/tool not found", file=sys.stderr)
        sys.exit(1)
    except acoustid.FingerprintGenerationError:
        print("fingerprint could not be calculated 1", file=sys.stderr)
        sys.exit(1)
    except acoustid.WebServiceError as exc:
        print("web service request failed:", exc.message, file=sys.stderr)
        sys.exit(1)

    final_results=[]

    first = True
    for score, rid, title, artist in results:
        if first:
            first = False
        else:
            pass
        t1= artist 
        t2= title
        t3= rid
        t4= int(score * 100)

        final_results.append([t1, t2, t3, t4])
        #print('%s - %s' % (artist, title))
        #print('http://musicbrainz.org/recording/%s' % rid)
        #print('Score: %i%%' % (int(score * 100)))

    print(final_results)

    score_sheet = []
    highest_score = final_results[0][3]

    for elt in final_results:
        if elt[3] == highest_score:
            score_sheet.append(elt)

    return score_sheet 

