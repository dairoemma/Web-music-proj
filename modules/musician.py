from modules.database import musicians_collection
from werkzeug.security import generate_password_hash, check_password_hash
from external_api.cloudinary_file import upload_music
from helper_function.utility import get_file__path
from flask import jsonify


def get_all_musician():
    musicians = musicians_collection.find()
    musician_dict = {musician["musician_name"]: musician for musician in musicians}
    return musician_dict


def get_musician(username):
    musician = musicians_collection.find_one({"musician_name": username})
    
    if musician:
        return musician
    else:
        return None


def insert_musician(musician_details):
    username = musician_details['username']
    password = musician_details['password']
    email = musician_details['email']
    music_genre = musician_details['music_genre'] 
    songs = musician_details['song']
    processed_songs=[]
    failed_songs = []

    if username and password and email and music_genre and songs:
        if get_musician(username=username):
            return jsonify({"status": "error", "message": "Username already exist"}), 400 
        
        result = get_file__path(songs=songs)
         
        if result['failed_song'] == None and result['processed_song'] == None:
            return jsonify({"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct"}), 400
        
        elif result['failed_song'] and result['processed_song']:
            for failed in result['failed_song']:
                failed_songs.append(failed)

        elif result['failed_song'] == None and result['processed_song']:
            for processed in result['processed_song']:
                processed_songs.append(processed)        
                
        hashed_password = generate_password_hash(password)
        musicians_collection.insert_one({
            "musician_name": username, 
            "password": hashed_password, 
            "email": email, 
            "music_genre": music_genre, 
            "music": processed_songs
            })
            
        if failed_songs:
            return jsonify({ "status": "success", "message": "Added musician but some songs failed to upload", "failed_songs": failed_songs }), 201
            
        else:

            return jsonify({"status": "success", "message": "musician added successfully. All songs uploaded successfully"}), 201
          
    else:

        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

def delete_user(musician_details):
    username = musician_details['username']
    password = musician_details['password']
    
    if username and password:
        musician_get_detail = get_musician(username=username)

        if musician_get_detail:
            
            if musician_get_detail['musician_name'] == username and check_password_hash(musician_get_detail['password'], password):
                musicians_collection.delete_one({"musician_name": username})
                return jsonify({"status": "success", "message": "musician deleted successfully"}), 200
            else:
                return jsonify({"status": "error", "message": "Incorrect username or password"}), 401
            
        else:
            return jsonify({"status": "error", "message": "musician does not exist"}), 400    
        
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

def update_musician(musician_details):
    username = musician_details['username']
    field_to_update = musician_details['field_to_update']
    field_new_value = musician_details['field_new_value']

    if username and field_to_update and field_new_value:
        if get_musician(username=username):
            musicians_collection.update_one({"musician_name": username}, {"$set": {field_to_update: field_new_value}})
            return jsonify({"status": "success", "message": "musician updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "musician does not exist"}), 400 
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

def update_music(music_details):
    username = music_details['username']
    song_name = music_details['song_name']
    new_song_link = music_details['new_song_link']

    if username and song_name and new_song_link:
        if get_musician(username=username):
            musicians_collection.update_one({"musician_name": username}, 
                                            {"$set": {"music.$[elem].song_link": new_song_link}}, 
                                            array_filter=[{'elem.song_name': song_name}]
                                            )
            return jsonify({"status": "success", "message": "music updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "musician does not exist"}), 400 
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
        

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
        return jsonify({"status": "error", "message": "All fields are required"}), 400


    
    

           
        
     
    
