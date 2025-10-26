from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Application Configuration
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # File Upload Configuration
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    allowed_file_types: List[str] = os.getenv("ALLOWED_FILE_TYPES", "pdf,txt,md,docx").split(",")
    
    # Vector Embeddings Configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    embedding_dimensions: int = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    class Config:
        env_file = ".env"

settings = Settings()
