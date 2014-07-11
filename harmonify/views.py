# imports

# import the django settings
from django.conf import settings
# for generating json
from django.utils import simplejson
# for loading template
from django.template import Context, loader
# for csrf
from django.core.context_processors import csrf
# for HTTP response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
import json
from harmonify.identify import music_identify
from harmonify.genre_list import glist
from harmonify.msearch import genre_query
from django.http import HttpResponseRedirect ,HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from harmonify.music_search import music_query
from harmonify.aidmatch import aidmatch
from harmonify.models import Profile, ListField
from harmonify.gracenote_query import get_gracenote_genre
from django.contrib.auth.models import User
import os, re
import uuid
import urllib
def custom_404(request):
    context = RequestContext(request)
    return render_to_response('userena/400.html',{},context)

def upload(request):
    """
    
    ## View for file uploads ##

    It does the following actions:
        - displays a template if no action have been specified
        - upload a file into unique temporary directory
                unique directory for an upload session
                    meaning when user opens up an upload page, all upload actions
                    while being on that page will be uploaded to unique directory.
                    as soon as user will reload, files will be uploaded to a different
                    unique directory
        - delete an uploaded file

    ## How Single View Multi-functions ##

    If the user just goes to a the upload url (e.g. '/upload/'), the request.method will be "GET"
        Or you can think of it as request.method will NOT be "POST"
    Therefore the view will always return the upload template

    If on the other side the method is POST, that means some sort of upload action
    has to be done. That could be either uploading a file or deleting a file

    For deleting files, there is the same url (e.g. '/upload/'), except it has an
    extra query parameter. Meaning the url will have '?' in it.
    In this implementation the query will simply be '?f=filename_of_the_file_to_be_removed'

    If the request has no query parameters, file is being uploaded.

    """

    # used to generate random unique id
    


    # settings for the file upload
    #   you can define other parameters here
    #   and check validity late in the code
    context = RequestContext(request)
    options = {
        # the maximum file size (must be in bytes)
        "maxfilesize": 2 * 2 ** 100, #
        # the minimum file size (must be in bytes)
        "minfilesize": 1 * 2 ** 10, # 1 Kb
        # the file types which are going to be allowed for upload
        #   must be a mimetype
        "acceptedformats": (
            'audio/basic',
            'audio/L24',
            'audio/mp3',
            'application/octet-stream',
            'audio/mp4',
            'audio/mpeg',
            'audio/ogg',
            'audio/vorbis',
            'audio/x-ms-wma',
            'audio/x-ms-wax',
            'audio/vnd.rn-realaudio',
            'audio/vnd.wave',
            'audio/webm'
            )
    }


    # POST request
    #   meaning user has triggered an upload action
    if request.method == 'POST':
        # figure out the path where files will be uploaded to
        # PROJECT_ROOT is from the settings file
        temp_path = os.path.join(settings.MEDIA_ROOT, "uploaded_music")

        # if 'f' query parameter is not specified
        # file is being uploaded
        if not ("f" in request.GET.keys()): # upload file

            # make sure some files have been uploaded
            if not request.FILES:
                return HttpResponseBadRequest('Must upload a file')

            # make sure unique id is specified - VERY IMPORTANT
            # this is necessary because of the following:
            #       we want users to upload to a unique directory
            #       however the uploader will make independent requests to the server
            #       to upload each file, so there has to be a method for all these files
            #       to be recognized as a single batch of files
            #       a unique id for each session will do the job
           

            # update the temporary path by creating a sub-folder within
            # the upload folder with the uid name

            # get the uploaded file
            file = request.FILES[u'files[]']

            # initialize the error
            # If error occurs, this will have the string error message so
            # uploader can display the appropriate message
            error = False

            # check against options for errors

            # file size
            if file.size > options["maxfilesize"]:
                error = "maxFileSize"
            if file.size < options["minfilesize"]:
                error = "minFileSize"
                # allowed file type
            if file.content_type not in options["acceptedformats"]:
                error = "acceptFileTypes"


            # the response data which will be returned to the uploader as json
            response_data = {
                "name": file.name,
                "size": file.size,
                "type": file.content_type
            }

            # if there was an error, add error message to response_data and return
            if error:
                # append error message
                response_data["error"] = error
                # generate json
                response_data = simplejson.dumps([response_data])
                # return response to uploader with error
                # so it can display error message
                return HttpResponse(response_data, mimetype='application/json')


            # make temporary dir if not exists already
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            # get the absolute path of where the uploaded file will be saved
            # all add some random data to the filename in order to avoid conflicts
            # when user tries to upload two files with same filename
            filename = os.path.join(temp_path, str(file.name))
            # open the file handler with write binary mode
            

            destination = open(filename, "wb+")
            # save file data into the disk
            # use the chunk method in case the file is too big
            # in order not to clutter the system memory
            for chunk in file.chunks():
                destination.write(chunk)
                # close the file
            destination.close()


            print filename


            #use this for EchoNest
            #music_response =  music_identify(filename)

            #use this for Acoustid + fpcalc + chromaprint
            music_response =  aidmatch(filename)

            print music_response




            #################################################
            #######  ACOUSTID PARSING
            #################################################
            song_list=[]
            for elt in music_response:
                song_list.append(elt[1])

            song_list = list(set(song_list))

            song_list = song_list[:3]


            song_artist_name = music_response[0][0]
            song_name = music_response[0][1]
            artist_link = 'http://musicbrainz.org/recording/' + music_response[0][2]

            #################################################
            #######  END ACOUSTID PARSING
            #################################################





            """
            # ##############################################
            #######  ECHONEST PARSING
            #################################################
            response_data = json.loads(music_response) 
            print response_data
              
            song_name = response_data['response']['songs'][0]['title']
            print song_name
            song_artist_name = response_data['response']['songs'][0]['artist_name']
            print song_artist_name
            song_artist_id = response_data['response']['songs'][0]['artist_id']
            print song_artist_id
            song_id = response_data['response']['songs'][0]['id']
            print song_id

            # ##############################################
            #######  END ECHONEST PARSING
            #################################################
            """


            #extract genre from file
            #if not found, then query Echonest
            from hsaudiotag import mpeg
            audio = mpeg.Mpeg(filename)
            artist_genre=""
            song_genre=""
            import string
            metadata_genre =  string.lower(str(audio.tag.genre))
            if(metadata_genre in glist):
                #
                #artist_genre = metadata_genre + " meta"

                song_genre = metadata_genre.lower().strip()
            else: 
                # use this for Acoustid + pygn
                song_genre =  get_gracenote_genre(song_artist_name, song_name).lower().strip()

                # use this for EchoNest
                #artist_genre = genre_query(song_artist_id)
            # use this for EchoNest
            #print artist_genre 

            # use this for Acoustid + pygn
            print song_genre 
            if song_genre == "urban":
                song_genre = "hip-hop"



            results = []
            user_list = []
            send_user_list = []
            if request.user and str(request.user) != "AnonymousUser":
                print "1"
                print type(request.user)
                print type(str(request.user))
                print str(request.user)
                print "1 end"
                all_user = User.objects.all().values_list('username', flat=True) 
                user = User.objects.get(username=request.user)
                try:
                    userprofile = Profile.objects.get(user=user)
                    if userprofile.genre:
                        if not song_genre in userprofile.genre:
                            userprofile.genre.append(song_genre)
                    else:
                        print "No genre in profile"
                        if not song_genre in userprofile.genre:
                            userprofile.genre.append(song_genre)
                    userprofile.save()
                    lst_genre = userprofile.genre
                    for one_user in all_user:
                        #print one_user
                        for genre in lst_genre:
                            #print genre
                            two_user = User.objects.get(username=request.user)
                            #print "1"
                            one_user_profile = Profile.objects.get(user=two_user)
                            #print "2"
                            if genre in one_user_profile.genre:
                                if one_user not in user_list:
                                    user_list.append(one_user)
                            else:
                                print "Some crazy error"
                    for send_user in user_list:
                        sed_user = User.objects.get(username=send_user)
                        sed_user_profile = Profile.objects.get(user=sed_user)
                        send_user_list.append({
                            "user":sed_user,
                            "profile":sed_user_profile
                            })
                    print user_list
                    print userprofile.genre
                except:
                    print "userprofile exception"
                    userprofile = None
            else:
                print "user not logged in"

                

            # use for Acoustid
            results.append({
                'artist':song_artist_name,
                'title':song_list,
                'artist_link':artist_link,
                'song_genre':song_genre
                })


            """
            # use for EchoNest
            results.append({
                'artist':song_artist_name,
                'title':song_name,
                'artist_id':song_artist_id,
                'song_id':song_id,
                'artist_genre':artist_genre
                })
            """

            # QUIRK HERE
            # in jQuey uploader, when it falls back to uploading using iFrames
            # the response content type has to be text/html
            # if json will be send, error will occur
            # if iframe is sending the request, it's headers are a little different compared
            # to the jQuery ajax request
            # they have different set of HTTP_ACCEPT values
            # so if the text/html is present, file was uploaded using jFrame because
            # that value is not in the set when uploaded by XHR
            if "text/html" in request.META["HTTP_ACCEPT"]:
                response_type = "text/html"

            # return the data to the uploading plugin
            return render_to_response('userena/music_search.html',{'result_list':results, 'send_user_list':send_user_list, 'request_user':str(request.user) },context)


        else: # file has to be deleted

            # get the file path by getting it from the query (e.g. '?f=filename.here')
            filepath = os.path.join(temp_path, request.GET["f"])

            # make sure file exists
            # if not return error
            if not os.path.isfile(filepath):
                return HttpResponseBadRequest("File does not exist")

            # delete the file
            # this step might not be a secure method so extra
            # security precautions might have to be taken
            os.remove(filepath)

            # generate true json result
            # in this case is it a json True value
            # if true is not returned, the file will not be removed from the upload queue
            response_data = simplejson.dumps(True)

            # return the result data
            # here it always has to be json
            return HttpResponse(response_data, mimetype="application/json")

    else: #GET
        # load the template
        return render_to_response('userena/upload.html',{},context)
# Create your views here.

def song_search(request):
    context = RequestContext(request)
    result_lst = []
    user_list = []
    send_user_list = []
    old_result_lst = []
    if request.method == 'POST':
        genre = request.POST['song_genre']
        artist_name = request.POST['artist']
        print artist_name
        song_name = request.POST['title']
        song_list = re.sub("u'|\[|\]|'|,", " ",song_name).strip().split('   ')
        if genre:
            result_lst = music_query(genre)
        old_result_lst.append({
            'artist_genre':genre,
            'artist_name':artist_name,
            'song_name':song_list
            })
        if request.user and str(request.user) != "AnonymousUser":
            print "1"
            print type(request.user)
            print type(str(request.user))
            print str(request.user)
            print "1 end"
            all_user = User.objects.all().values_list('username', flat=True) 
            user = User.objects.get(username=request.user)
            try:
                userprofile = Profile.objects.get(user=user)
                if userprofile.genre:
                    if not genre in userprofile.genre:
                            userprofile.genre.append(genre)
                else:
                    print "No genre in profile"
                    if not genre in userprofile.genre:
                        userprofile.genre.append(genre)
                userprofile.save()
                lst_genre = userprofile.genre
                for one_user in all_user:
                    #print one_user
                    for genre in lst_genre:
                        #print genre
                        two_user = User.objects.get(username=request.user)
                        #print "1"
                        one_user_profile = Profile.objects.get(user=two_user)
                        #print "2"
                        if genre in one_user_profile.genre:
                            if one_user not in user_list:
                                user_list.append(one_user)
                        else:
                            print "Some crazy error"
                for send_user in user_list:
                    sed_user = User.objects.get(username=send_user)
                    sed_user_profile = Profile.objects.get(user=sed_user)
                    send_user_list.append({
                        "user":sed_user,
                        "profile":sed_user_profile
                        })
                print user_list
                print userprofile.genre
            except:
                print "userprofile exception"
                userprofile = None
        else:
            print "user not logged in"
        
        return render_to_response('userena/music_search.html',{'result_lst':result_lst, 'old_result_lst':old_result_lst, "send_user_list":send_user_list },context)
    else:
        return custom_404(request)