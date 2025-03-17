import cloudinary
from cloudinary.uploader import upload
from config import Config


cloudinary.config(
    cloud_name = Config.Cloud_name,
    api_key = Config.Api_key,
    api_secret = Config.Api_secret
)


def upload_music(file_path):

    try:
       
       response =  upload(file_path, resource_type="auto")
       audio_url = response.get("secure_url")
       return audio_url
    
    except Exception as e:
        
        print(f"an error occured: {e}")
        return None