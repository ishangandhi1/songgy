



def echonest_parsedata():

            # generate the json data
            response_data = json.loads(music_response)
            # response 
            print response_data
            
                    
            song_name = response_data['response']['songs'][0]['title']
            print song_name
            song_artist_name = response_data['response']['songs'][0]['artist_name']
            print song_artist_name
            song_artist_id = response_data['response']['songs'][0]['artist_id']
            print song_artist_id
            song_id = response_data['response']['songs'][0]['id']
            print song_id