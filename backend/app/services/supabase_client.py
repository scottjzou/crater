from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        self.service_client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
    
    def get_client(self) -> Client:
        return self.client
    
    def get_service_client(self) -> Client:
        return self.service_client
    
    async def upload_file(self, bucket: str, file_path: str, file_data: bytes) -> str:
        """Upload file to Supabase Storage"""
        try:
            response = self.service_client.storage.from_(bucket).upload(
                file_path, file_data
            )
            return response
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    async def download_file(self, bucket: str, file_path: str) -> bytes:
        """Download file from Supabase Storage"""
        try:
            response = self.service_client.storage.from_(bucket).download(file_path)
            return response
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            raise
    
    async def delete_file(self, bucket: str, file_path: str) -> bool:
        """Delete file from Supabase Storage"""
        try:
            self.service_client.storage.from_(bucket).remove([file_path])
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    async def get_public_url(self, bucket: str, file_path: str) -> str:
        """Get public URL for file"""
        try:
            response = self.service_client.storage.from_(bucket).get_public_url(file_path)
            return response
        except Exception as e:
            logger.error(f"Error getting public URL: {e}")
            raise

# Global instance
supabase_client = SupabaseClient()
