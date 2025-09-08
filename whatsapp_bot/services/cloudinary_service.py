import cloudinary
import os
 
class CloudinaryService:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )
    
    @staticmethod
    def upload_audio(file_path: str) -> str:
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type="video",
                folder="voice_responses"
            )
            return result.get("secure_url")
        except Exception as e:
            return f"Upload failed: {str(e)}"
