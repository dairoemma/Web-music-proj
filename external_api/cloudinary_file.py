# importing cloudianry dependency
import cloudinary
from cloudinary.uploader import upload
from config import Config #importing config to configure the cloudinary

# configure cloudinary
cloudinary.config(
    cloud_name = Config.Cloud_name,
    api_key = Config.Api_key,
    api_secret = Config.Api_secret
)

# function to handle the uploading of music
def upload_music(file_path):

    try:
       
       response =  upload(file_path, resource_type="auto") #upload the filepath given to cloudianry
       audio_url = response.get("secure_url") #get the cloudinary generated url
       return audio_url # return the url
    
    except Exception as e:
        
        print(f"an error occured: {e}")
        return None