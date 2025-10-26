from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ContentType(str, Enum):
    BLOG_POST = "blog_post"
    SUMMARY = "summary"
    FAQ = "faq"
    SOCIAL_MEDIA = "social_media"
    STUDY_GUIDE = "study_guide"
    CUSTOM = "custom"

class DocumentBase(BaseModel):
    title: str
    file_type: str
    folder_path: Optional[str] = None
    tags: List[str] = []

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    folder_path: Optional[str] = None
    tags: Optional[List[str]] = None

class Document(DocumentBase):
    id: str
    user_id: str
    file_path: str
    extracted_text: Optional[str] = None
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    chunk_text: str
    chunk_index: int
    metadata: Dict[str, Any] = {}

class DocumentLink(BaseModel):
    id: str
    source_doc_id: str
    target_doc_id: str
    link_type: str = "reference"

class TemplateBase(BaseModel):
    name: str
    prompt_template: str
    parameters: Dict[str, Any] = {}
    is_public: bool = False

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    prompt_template: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None

class Template(TemplateBase):
    id: str
    user_id: str
    usage_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GeneratedDocBase(BaseModel):
    title: str
    content: str
    template_id: Optional[str] = None
    source_doc_ids: List[str] = []
    toc: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = {}

class GeneratedDocCreate(GeneratedDocBase):
    pass

class GeneratedDocUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class GeneratedDoc(GeneratedDocBase):
    id: str
    user_id: str
    version: int = 1
    status: str = "draft"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocVersion(BaseModel):
    id: str
    generated_doc_id: str
    content: str
    version_number: int
    created_at: datetime
    created_by: str

class ContentGenerationRequest(BaseModel):
    source_doc_ids: List[str]
    template_id: Optional[str] = None
    custom_prompt: Optional[str] = None
    output_format: Optional[str] = None
    parameters: Dict[str, Any] = {}

class ContentGenerationResponse(BaseModel):
    toc: Dict[str, Any]
    style_guide: Dict[str, Any]
    example_snippet: str
    source_citations: List[str]
    estimated_tokens: int

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
