import cloudinary
from decouple import config

cloudinary.config(
  cloud_name=config('CLOUD_NAME'),
  api_key=config('API_KEY'),
  api_secret=config('API_SECRET')
)
cloudinary_cloud_name=config('CLOUD_NAME')
cloudinary_url = f"https://api.cloudinary.com/v1_1/{cloudinary_cloud_name}/image/upload"