from external_api.cloudinary_file import upload_music
from modules.musician import get_all_musician, get_musician, get_music, get_a_music
from modules.user import get_all_user, get_user


def get_file__path(songs):
    processed_song = []
    failed_song = []

    if songs:
        for song in songs:
            song_name = song.get('song_name')
            song_file_path = song.get('song_file_path')
        
            if song_file_path:
                song_url =  upload_music(song_file_path)
                
                if song_url:
                    processed_song.append({
                    "song_name":song_name,
                    "song_link": song_url
                    })   

                else:
                    
                    failed_song.append(f" failed to upload: {song_name}")
                    continue
                
            else:   

                failed_song.append(f" Missing file path for: {song_name}")
                continue   

        if not processed_song:
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct", "failed_song": None, "processed_song": None}
                
        if failed_song:

            return { "status": "error", "message":"some songs failed to uplaod","failed_song": failed_song, "processed_song": processed_song }
            
        else:

            return {"status": "success", "message": "All songs uploaded successfully", "failed_song": failed_song, "processed_song": processed_song}
          
    else:    
        return {"status": "error", "message": "Enter song details","failed_song": None, "processed_song": None}
    

def search_musician(unique_name, musician_name):
    if unique_name:

        if musician_name:

            musician_details = get_musician(musician_name)

            if musician_details:
                return {musician_details}, 200
            else:
                return {"status": "error", "message": "Musician not found"}, 404
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401

   
def search_user(unique_name, user_to_search):
    if unique_name:

        if user_to_search:

            user_details = get_user(user_to_search)

            if user_details:
                return {user_details}, 200
            else:
                return {"status": "error","message": "User not found"}, 404
            
        else:
            return {"status": "error", "message": "All fieds required"}, 400
        
    else:
        return {"status": "error", "message": "Invalid Credentials, Access denied"}, 401 


def get_all_users(unique_name):
    if unique_name:
        users_details = get_all_user()
        return {users_details}, 200
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401


def get_musicians(unique_name):  
    if unique_name:
        musicians_details = get_all_musician()
        return {musicians_details}, 200
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401
    

def search_music(unique_name, music_detail):
    if unique_name:

        if music_detail:

            music = get_a_music(music_detail)

            if music:
                return {music}, 200
            else:
                return {"status": "error", "message": "Music not found"}, 404
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401    


def get_musician_catalogue(unique_name, musician_name):
    if unique_name:

        if musician_name:
            music_details = get_music(musician_name)

            if music_details:
                return {music_details}, 200
            else:
                return {"status": "error", "message": "Musician not found"}, 404
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400    
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401
    


    