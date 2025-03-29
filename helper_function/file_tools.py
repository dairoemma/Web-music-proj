from external_api.cloudinary_file import upload_music  #import the upload music function from the cloudinary file


# this function receives the file path and song name, and then sends the file path for processing and returns both the song name and path for easy input to the database
# this function was initially in the utility.py which was suppose to be where we had all our overused helper functions but it caused a circular import so it was kept in a seperate file which is this file
def get_file__path(song_name, temp_path):
    processed_song = [] #list for the processed songs
    failed_song = [] #list for the failed songs

    if song_name and temp_path:
            
        if temp_path:
            song_url =  upload_music(temp_path) #sending filepath to cloudinary upload_music function to get the cloudinary url
                
            if song_url:
                processed_song.append({
                "song_name":song_name,
                "song_link": song_url
                })   # add the song name and song url to processed song if song url is not none

            else:    
                
                failed_song.append(f" failed to upload: {song_name}") #add the song name  to failed songif song_url is none
                
        else:   

            failed_song.append(f" Missing file path for: {song_name}") #add the song name to failed song if no file path was given
            
        # this sends processed song as none so we can check that when we call it in other part of the code.
        if not processed_song:
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct", "processed_song": None}
                # it returns failed songs that the name of the song that failed 
        if failed_song:

            return { "status": "error", "message":"some songs failed to uplaod","failed_song": failed_song }
            #  this would return only when all the songs uploaded so failed song would be none
        else:

            return {"status": "success", "message": "All songs uploaded successfully", "processed_song": processed_song}
        #   this was for cases where the function was called without no argument which means there would be no value to add to the list so they should both return none in that scenario
    else:    
        return {"status": "error", "message": "Enter song details","failed_song": None, "processed_song": None}
    