from modules.database import musicians_collection
from werkzeug.security import generate_password_hash, check_password_hash
from helper_function.file_tools import get_file__path

def get_all_musician():
    musicians = musicians_collection.find()
    musician_dict = {musician["musician_name"]: musician for musician in musicians}
    return musician_dict


def get_musician(username):
    musician = musicians_collection.find_one({"musician_name": username})
    
    if musician:
        return musician
    else:
        return {"status": "error", "message": "Artist name doesn't exist"}, 404


def insert_musician(musician_details):
    username = musician_details['username']
    password = musician_details['password']
    email = musician_details['email']
    music_genre = musician_details['music_genre'] 
    
    if username and password and email and music_genre:
        musician = get_musician(username)
        if isinstance(musician, dict) and musician.get("status") != "error":
            return {"status": "error", "message": "Username already exist"}, 400
        else:
            hashed_password = generate_password_hash(password)
            musicians_collection.insert_one({
            "musician_name": username, 
            "password": hashed_password, 
            "email": email, 
            "music_genre": music_genre
            })
            return {"status": "success", "message": "musician added successfully"}, 201

    else:
        return {"status": "error", "message": "All fields are required"}, 400          
    

def delete_musician(username, password):
    if username and password:
        musician_get_detail = get_musician(username=username)

        if musician_get_detail:
            
            if musician_get_detail['musician_name'] == username and check_password_hash(musician_get_detail['password'], password):
                musicians_collection.delete_one({"musician_name": username})
                return {"status": "success", "message": "musician deleted successfully"}, 200
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "musician does not exist"}, 404    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
def delete_music(username, password, song_name):
    if username and password and song_name:
        musician_get_detail = get_musician(username=username)

        if musician_get_detail:
            
            if musician_get_detail['musician_name'] == username and check_password_hash(musician_get_detail['password'], password):
                musicians_collection.update_one({"musician_name": username},
                                                 {"$pull": {"music": {"song_name":song_name }}}
                                                 )
                return {"status": "success", "message": "music deleted successfully"}, 200
            
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "musician does not exist"}, 404    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

def update_musician(username, musician_details):
    field_to_update = musician_details['field_to_update']
    field_new_value = musician_details['field_new_value']

    if username and field_to_update and field_new_value:

        musician = get_musician(username)
        if isinstance(musician, dict) and musician.get("status") != "error":
            if field_to_update == "password":
               musician_password = field_new_value
               hashed_password = generate_password_hash(musician_password)
               musicians_collection.update_one({"musician_name": username}, {"$set": {"password": hashed_password}})
               return {"status": "success", "message": "musician password updated successfully"}, 200
            else:
                musicians_collection.update_one({"musician_name": username}, {"$set": {field_to_update: field_new_value}})
                return {"status": "success", "message": "musician updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
def update_music(username,song_name, temp_path ):
    failed_songs = []
    is_processed = None

    if username and song_name and temp_path:

        if get_musician(username=username):
            result = get_file__path(song_name, temp_path) 

            if result['failed_song'] == None and result['processed_song'] == None:
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct"}, 400
        
            elif result['failed_song']:
                for failed in result['failed_song']:
                    failed_songs.append(failed)
                    return { "status": "error", "message": "some songs failed to upload", "failed_songs": failed_songs }, 400

            elif result['failed_song'] == None and result['processed_song']:
                for processed in result['processed_song']:
                    musicians_collection.update_one({"musician_name": username}, 
                                            {"$set": {"music.$[elem].song_link": processed['song_link']}}, 
                                            array_filter=[{'elem.song_name': song_name}]
                                            )
                is_processed  = True
                    
            if is_processed:
                return {"status": "success", "message": "music updated successfully"}, 201      
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
        

def add_music(username, song_name, temp_path):       
    processed_songs=[]
    failed_songs = []

    if username and song_name and temp_path:

        if get_musician(username=username):
            result = get_file__path(song_name, temp_path) 

            if result['failed_song'] == None and result['processed_song'] == None:
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct"}, 400
        
            elif result['failed_song']:
                for failed in result['failed_song']:
                    failed_songs.append(failed)
                    return { "status": "error", "message": "some songs failed to upload", "failed_songs": failed_songs }, 400

            elif result['failed_song'] == None and result['processed_song']:
                for processed in result['processed_song']:
                    processed_songs.append(processed)
                    
            if processed_songs:
                musicians_collection.update_one({"musician_name": username}, 
                                            {"$set": {"music": processed_songs}}
                                            )
                return {"status": "success", "message": "musician added successfully"}, 201      
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400 


def get_music(username):
    musician =  musicians_collection.find_one({"musician_name": username})

    if musician:
        music = musician.get('music', [])

        songs = { song["song_name"]: song["song_link"] for song in music}
        return songs
    
    else:
        return None
    

def get_a_music(details):
    musician = details['musician_name']
    name_of_song = details['name_of_song']

    if musician and name_of_song:
        music_requested = musicians_collection.find_one({"musician_name": musician, "music.song_name": name_of_song}, {"music.$": 1})

        if music_requested:
            song = music_requested.get('music', [])[0]
            return song.get("song_link")
        
        else:
            return None
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
