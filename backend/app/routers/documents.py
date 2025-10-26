from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from typing import List, Optional
from app.models.schemas import Document, DocumentCreate, DocumentUpdate, DocumentStatus
from app.services.supabase_client import supabase_client
from app.services.pdf_processor import pdf_processor
from app.routers.auth import get_current_user, User
import logging
import uuid
import os

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    folder_path: Optional[str] = Form(None),
    tags: Optional[str] = Form(""),
    current_user: User = Depends(get_current_user)
):
    """Upload and process a document"""
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in ["pdf", "txt", "md", "docx"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Read file data
        file_data = await file.read()
        
        # Generate unique file path
        file_id = str(uuid.uuid4())
        file_path = f"documents/{current_user.id}/{file_id}.{file_extension}"
        
        # Upload to Supabase Storage
        await supabase_client.upload_file("documents", file_path, file_data)
        
        # Process file based on type
        extracted_text = ""
        if file_extension == "pdf":
            pdf_data = await pdf_processor.process_pdf(file_data)
            extracted_text = pdf_data["text"]
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
        
        # Create document record
        document_data = {
            "id": file_id,
            "user_id": current_user.id,
            "title": title,
            "file_path": file_path,
            "file_type": file_extension,
            "folder_path": folder_path,
            "tags": tag_list,
            "extracted_text": extracted_text,
            "status": DocumentStatus.COMPLETED.value if extracted_text else DocumentStatus.PROCESSING.value
        }
        
        # Save to database
        response = supabase_client.get_service_client().table("documents").insert(document_data).execute()
        
        return Document(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload document")

@router.get("/", response_model=List[Document])
async def get_documents(
    folder_path: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """Get user's documents with optional filtering"""
    try:
        query = supabase_client.get_client().table("documents").select("*").eq("user_id", current_user.id)
        
        if folder_path:
            query = query.eq("folder_path", folder_path)
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            query = query.contains("tags", tag_list)
        
        response = query.order("created_at", desc=True).execute()
        return [Document(**doc) for doc in response.data]
        
    except Exception as e:
        logger.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch documents")

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific document"""
    try:
        response = supabase_client.get_client().table("documents").select("*").eq("id", document_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return Document(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error fetching document: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch document")

@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update document metadata"""
    try:
        # Check if document exists and belongs to user
        existing = supabase_client.get_client().table("documents").select("*").eq("id", document_id).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Update document
        update_data = document_update.dict(exclude_unset=True)
        response = supabase_client.get_client().table("documents").update(update_data).eq("id", document_id).eq("user_id", current_user.id).execute()
        
        return Document(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        raise HTTPException(status_code=500, detail="Failed to update document")

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a document"""
    try:
        # Get document info
        response = supabase_client.get_client().table("documents").select("file_path").eq("id", document_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = response.data[0]["file_path"]
        
        # Delete from storage
        await supabase_client.delete_file("documents", file_path)
        
        # Delete from database
        supabase_client.get_client().table("documents").delete().eq("id", document_id).eq("user_id", current_user.id).execute()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete document")

@router.get("/folders/list")
async def get_folders(current_user: User = Depends(get_current_user)):
    """Get list of folders"""
    try:
        response = supabase_client.get_client().table("documents").select("folder_path").eq("user_id", current_user.id).execute()
        
        folders = set()
        for doc in response.data:
            if doc["folder_path"]:
                folders.add(doc["folder_path"])
        
        return {"folders": sorted(list(folders))}
        
    except Exception as e:
        logger.error(f"Error fetching folders: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch folders")

@router.get("/tags/list")
async def get_tags(current_user: User = Depends(get_current_user)):
    """Get list of tags"""
    try:
        response = supabase_client.get_client().table("documents").select("tags").eq("user_id", current_user.id).execute()
        
        tags = set()
        for doc in response.data:
            if doc["tags"]:
                tags.update(doc["tags"])
        
        return {"tags": sorted(list(tags))}
        
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tags")
