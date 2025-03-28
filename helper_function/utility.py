from modules.musician import get_all_musician, get_musician, get_music, get_a_music
from modules.user import get_all_user, get_user


def search_musician(unique_name, musician_name):
    if unique_name:

        if musician_name:

            musician_details = get_musician(musician_name)

            if musician_details:
                musician_details['_id'] = str(musician_details['_id'])
                return musician_details, 200
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
                user_details['_id'] = str(user_details['_id'])
                return user_details, 200
            else:
                return {"status": "error","message": "User not found"}, 404
            
        else:
            return {"status": "error", "message": "All fieds required"}, 400
        
    else:
        return {"status": "error", "message": "Invalid Credentials, Access denied"}, 401 


def get_all_users(unique_name):
    if unique_name:
        users_details = get_all_user()
        return users_details, 200
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401


def get_musicians(unique_name):  
    if unique_name:
        musicians_details = get_all_musician()
        return musicians_details, 200
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
                return music_details, 200
            else:
                return {"status": "error", "message": "Musician not found"}, 404
            
        else:
            return {"status": "error", "message": "All fields are required"}, 400    
        
    else:
        return {"status": "error", "message": "Invalid credentials, Access denied"}, 401
    


    