from external_api.cloudinary_file import upload_music
from flask import jsonify


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
    



    