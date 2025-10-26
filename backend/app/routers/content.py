from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from app.models.schemas import (
    GeneratedDoc, GeneratedDocCreate, GeneratedDocUpdate,
    ContentGenerationRequest, ContentGenerationResponse
)
from app.services.supabase_client import supabase_client
from app.services.content_generator import content_generator
from app.routers.auth import get_current_user, User
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate/preview", response_model=ContentGenerationResponse)
async def generate_content_preview(
    request: ContentGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate content preview (ToC, style, example snippet)"""
    try:
        # Get source documents
        response = supabase_client.get_client().table("documents").select("*").in_("id", request.source_doc_ids).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Source documents not found")
        
        # Get document chunks (simplified - in production, retrieve from vector DB)
        chunks = []
        for doc in response.data:
            if doc["extracted_text"]:
                chunks.append({
                    "text": doc["extracted_text"],
                    "document_id": doc["id"],
                    "title": doc["title"]
                })
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text content found in source documents")
        
        # Generate preview
        preview = await content_generator.generate_content_preview(
            chunks,
            request.template_id,  # Would need to fetch template prompt
            request.custom_prompt,
            request.output_format
        )
        
        return ContentGenerationResponse(**preview)
        
    except Exception as e:
        logger.error(f"Error generating content preview: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate content preview")

@router.post("/generate", response_model=GeneratedDoc)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Generate full content"""
    try:
        # Get source documents
        response = supabase_client.get_client().table("documents").select("*").in_("id", request.source_doc_ids).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Source documents not found")
        
        # Get document chunks
        chunks = []
        for doc in response.data:
            if doc["extracted_text"]:
                chunks.append({
                    "text": doc["extracted_text"],
                    "document_id": doc["id"],
                    "title": doc["title"]
                })
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text content found in source documents")
        
        # Generate content
        content = await content_generator.generate_full_content(
            chunks,
            request.template_id,  # Would need to fetch template prompt
            request.custom_prompt
        )
        
        # Create generated document record
        doc_id = str(uuid.uuid4())
        generated_doc_data = {
            "id": doc_id,
            "user_id": current_user.id,
            "title": f"Generated Content {doc_id[:8]}",
            "content": content,
            "template_id": request.template_id,
            "source_doc_ids": request.source_doc_ids,
            "metadata": request.parameters,
            "version": 1,
            "status": "draft"
        }
        
        # Save to database
        response = supabase_client.get_client().table("generated_docs").insert(generated_doc_data).execute()
        
        return GeneratedDoc(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate content")

@router.get("/", response_model=List[GeneratedDoc])
async def get_generated_documents(
    current_user: User = Depends(get_current_user)
):
    """Get user's generated documents"""
    try:
        response = supabase_client.get_client().table("generated_docs").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return [GeneratedDoc(**doc) for doc in response.data]
        
    except Exception as e:
        logger.error(f"Error fetching generated documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch generated documents")

@router.get("/{doc_id}", response_model=GeneratedDoc)
async def get_generated_document(
    doc_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific generated document"""
    try:
        response = supabase_client.get_client().table("generated_docs").select("*").eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Generated document not found")
        
        return GeneratedDoc(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error fetching generated document: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch generated document")

@router.put("/{doc_id}", response_model=GeneratedDoc)
async def update_generated_document(
    doc_id: str,
    doc_update: GeneratedDocUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update generated document"""
    try:
        # Check if document exists and belongs to user
        existing = supabase_client.get_client().table("generated_docs").select("*").eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Generated document not found")
        
        # Update document
        update_data = doc_update.dict(exclude_unset=True)
        response = supabase_client.get_client().table("generated_docs").update(update_data).eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        return GeneratedDoc(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error updating generated document: {e}")
        raise HTTPException(status_code=500, detail="Failed to update generated document")

@router.post("/{doc_id}/refine")
async def refine_content(
    doc_id: str,
    refinement_prompt: str,
    current_user: User = Depends(get_current_user)
):
    """Refine existing content"""
    try:
        # Get existing document
        response = supabase_client.get_client().table("generated_docs").select("*").eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Generated document not found")
        
        doc = response.data[0]
        
        # Refine content
        refined_content = await content_generator.refine_content(
            doc["content"],
            refinement_prompt
        )
        
        # Update document with refined content
        update_data = {
            "content": refined_content,
            "version": doc["version"] + 1
        }
        
        response = supabase_client.get_client().table("generated_docs").update(update_data).eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        return GeneratedDoc(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error refining content: {e}")
        raise HTTPException(status_code=500, detail="Failed to refine content")

@router.delete("/{doc_id}")
async def delete_generated_document(
    doc_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete generated document"""
    try:
        # Check if document exists and belongs to user
        existing = supabase_client.get_client().table("generated_docs").select("*").eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Generated document not found")
        
        # Delete from database
        supabase_client.get_client().table("generated_docs").delete().eq("id", doc_id).eq("user_id", current_user.id).execute()
        
        return {"message": "Generated document deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting generated document: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete generated document")
