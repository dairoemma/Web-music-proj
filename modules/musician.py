from modules.database import musicians_collection
from werkzeug.security import generate_password_hash, check_password_hash
from helper_function.file_tools import get_file__path

#function to get all the musician from the database
def get_all_musician():
    musicians = musicians_collection.find() #query to search the musicians collection and return all document
    musician_dict = {}

    for musician in musicians:
        musician['_id'] = str(musician['_id'])  
        musician_dict[musician["musician_name"]] = musician  # store the musician in a dict

    return musician_dict #return the dict


#function to get a musician from the database
def get_musician(username):
    musician = musicians_collection.find_one({"musician_name": username})#the query to search the musicians collection and return a musician document
    
    if musician:
        return musician #return the musician
    else:
        return {"status": "error", "message": "Artist name doesn't exist"}, 404


#function to insert a musician to the database
def insert_musician(musician_details):
    # get all the details
    username = musician_details['username']
    password = musician_details['password']
    email = musician_details['email']
    music_genre = musician_details['music_genre'] 
    
    if username and password and email and music_genre:
        musician = get_musician(username) #we used the get musician to check if the musician already exist
        if isinstance(musician, dict) and musician.get("status") != "error":
            return {"status": "error", "message": "Username already exist"}, 400 #return an error musician name (username) already exist response and 400 status code
        else:
            hashed_password = generate_password_hash(password) #generate the hashed password
            musicians_collection.insert_one({
            "musician_name": username, 
            "password": hashed_password, 
            "email": email, 
            "music_genre": music_genre
            }) #run the query to insert the musician
            return {"status": "success", "message": "musician added successfully"}, 201

    else:
        return {"status": "error", "message": "All fields are required"}, 400          
    

#function to delete a musician in the database
def delete_musician(username, password=None, force=False):
    musician = get_musician(username=username) # check if musician already exist

    if not musician:
        return {"status": "error", "message": "Musician does not exist"}, 404 #return musician doesn't exist if user is none

    if force or (password and check_password_hash(musician['password'], password)): #check if the username and the username password matches the musician and is password given and if force is true to give admin priviledge
        musicians_collection.delete_one({"musician_name": username})
        return {"status": "success", "message": "Musician deleted successfully"}, 200 #run the query to delete the musician
    else:
        return {"status": "error", "message": "Incorrect password"}, 401


#function to delete a music in the database    
def delete_music(username, password, song_name):
    if username and password and song_name:
        musician_get_detail = get_musician(username=username) # check if musician already exist

        if musician_get_detail:
            
            if musician_get_detail['musician_name'] == username and check_password_hash(musician_get_detail['password'], password): #check if the username and the username password matches the musician and is password given
                musicians_collection.update_one({"musician_name": username},
                                                 {"$pull": {"music": {"song_name":song_name }}}
                                                 ) #run the query to delete the music
                return {"status": "success", "message": "music deleted successfully"}, 200
            
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "musician does not exist"}, 404    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

#function to update a musician in the database
def update_musician(username, musician_details):
    # get all the details
    field_to_update = musician_details['field_to_update']
    field_new_value = musician_details['field_new_value']

    if username and field_to_update and field_new_value:

        musician = get_musician(username) #we used the get musician to check if the musician already exist exist
        if isinstance(musician, dict) and musician.get("status") != "error":
            if field_to_update == "password": # if field to update is the password, it should update it seperately because we want to hash the password first
               musician_password = field_new_value
               hashed_password = generate_password_hash(musician_password)
               musicians_collection.update_one({"musician_name": username}, {"$set": {"password": hashed_password}})#run the query to update the password
               return {"status": "success", "message": "musician password updated successfully"}, 200
            else:
                musicians_collection.update_one({"musician_name": username}, {"$set": {field_to_update: field_new_value}})#run the query to update the musician
                return {"status": "success", "message": "musician updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

#function to update a music in the database    
def update_music(username,song_name, temp_path ):
    is_processed = None

    if username and song_name and temp_path:

        if get_musician(username=username): #we used the get musician to check if the musician already exist exist
            result = get_file__path(song_name, temp_path) #get the response of the get file path

            if not result or result['processed_song'] == None: #check if song wasn't able to upload
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct"}, 400

            elif result['processed_song']: #check if song uploaded
                for processed in result['processed_song']:
                    musicians_collection.update_one({"musician_name": username}, 
                                            {"$set": {"music.$[elem].song_link": processed['song_link']}}, 
                                            array_filters=[{'elem.song_name': song_name}]
                                            )# run the query to update the music
                is_processed  = True
                    
            if is_processed:
                return {"status": "success", "message": "music updated successfully"}, 201  #return success message and status code if is processed which means music was updated   
             
            return { "status": "error","message": result.get("message", "Upload failed"),"details": result}, 400 #return an error message if it failed to update
        
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
        
#function to add a music to the database 
def add_music(username, song_name, temp_path):       
    processed_songs=[]
  

    if username and song_name and temp_path:

        if get_musician(username=username): #we used the get musician to check if the musician already exist exist
            result = get_file__path(song_name, temp_path) #get the response of the get file path

            if not result or result['processed_song'] == None: #check if song wasn't able to upload
                return {"status": "error", "message": "Couldn't upload any song , check your file path and make sure it is correct"}, 400

            elif result['processed_song']: #check if song uploaded
                for processed in result['processed_song']:
                    processed_songs.append(processed)
                    
            if processed_songs:
                musicians_collection.update_one({"musician_name": username}, 
                                            {"$push": {"music": {"$each": processed_songs}}}
                                            )# run the query to add the music
                return {"status": "success", "message": "musician added successfully"}, 201  #return success message and status code if music was added
             
            return { "status": "error","message": result.get("message", "Upload failed"),"details": result}, 400   #return an error message if it failed to add music
        else:
            return {"status": "error", "message": "musician does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400 


#function to get music from the database 
def get_music(username):
    musician =  musicians_collection.find_one({"musician_name": username}) #the query to search the musicians collection and return a musician document

    if musician:
        music = musician.get('music', []) #get the music field
        # make music a list of dict
        songs = { song["song_name"]: song["song_link"] for song in music} #since music field is embeded in the document this means it an array so we iterate and store the songname ass key and song link as item
        return songs #return the songs
    
    else:
        return None
    

#function to get a music from the database 
def get_a_music(details):
    # get all the details
    musician = details['musician_name']
    name_of_song = details['name_of_song']
    
    if musician and name_of_song:
        music_requested = musicians_collection.find_one({"musician_name": musician, "music.song_name": name_of_song}, {"music.$": 1}) #run the query to find the first song with that songname in the document
        
        if music_requested:
            song = music_requested.get('music', [])[0] #this makes sure it the exact song that is gotten
            return song.get("song_link") #return the song link
        
        else:
            return None
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
