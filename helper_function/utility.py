from modules.musician import get_all_musician, get_musician, get_music, get_a_music
from modules.user import get_all_user, get_user

# search musician helper function
def search_musician(unique_name, musician_name):
    if unique_name: #validate if the jwt_identity was given

        if musician_name:

            musician_details = get_musician(musician_name) #get the details of musician
            #  check if musician exist
            if musician_details: 
                musician_details['_id'] = str(musician_details['_id']) #change the mongodb bson _id to string so json can read it
                return musician_details, 200 #return musician details
            else:
                return {"status": "error", "message": "Musician not found"}, 404 #return musician not found and it status code if musician details is none
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400 #return error message if musician name not given
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401 #return 401 error for an unathorized access

# search user helper function   
def search_user(unique_name, user_to_search):
    if unique_name: #validate if the jwt_identity was given

        if user_to_search:

            user_details = get_user(user_to_search) #get the details of user
             #  check if user exist
            if user_details:
                user_details['_id'] = str(user_details['_id'])#change the mongodb bson _id to string so json can read it
                return user_details, 200 #return user details
            else:
                return {"status": "error","message": "User not found"}, 404 #return user not found and it status code if user details is none
            
        else:
            return {"status": "error", "message": "All fieds required"}, 400 #return error message if user name not given
        
    else:
        return {"status": "error", "message": "Invalid Credentials, Access denied"}, 401 #return 401 error for an unathorized access

# get all user helper function  
def get_all_users(unique_name):
    if unique_name: #validate if the jwt_identity was given
        users_details = get_all_user() #get the details ofall users
        return users_details, 200 #return users details
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401 #return 401 error for an unathorized access

# get musician helper function  
def get_musicians(unique_name):  
    if unique_name:  #validate if the jwt_identity was given
        musicians_details = get_all_musician() #get the details of all musicians
        return musicians_details, 200 #return musicians details
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401 #return 401 error for an unathorized access
    
# search music helper function   
def search_music(unique_name, music_detail):
    if unique_name: #validate if the jwt_identity was given

        if music_detail:

            music = get_a_music(music_detail) #get the details of music

            if music:
                return {music}, 200 #return the music
            else:
                return {"status": "error", "message": "Music not found"}, 404 #return music not found and it status code if music is none
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400 #return error message if music detail not given
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401 #return 401 error for an unathorized access   

# get_musician_catalogue helper function 
def get_musician_catalogue(unique_name, musician_name):
    if unique_name: #validate if the jwt_identity was given

        if musician_name:
            music_details = get_music(musician_name) #get the details of music

            if music_details:
                return music_details, 200 #return the music details
            else:
                return {"status": "error", "message": "Musician not found"}, 404 #return musician not found and it status code if music details is none
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400    #return error message if musician name not given
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401 #return 401 error for an unathorized access
    


    