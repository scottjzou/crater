from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.schemas import Template, TemplateCreate, TemplateUpdate
from app.services.supabase_client import supabase_client
from app.routers.auth import get_current_user, User
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Template)
async def create_template(
    template: TemplateCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new template"""
    try:
        template_data = {
            "id": str(uuid.uuid4()),
            "user_id": current_user.id,
            **template.dict()
        }
        
        response = supabase_client.get_client().table("templates").insert(template_data).execute()
        return Template(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error creating template: {e}")
        raise HTTPException(status_code=500, detail="Failed to create template")

@router.get("/", response_model=List[Template])
async def get_templates(
    current_user: User = Depends(get_current_user)
):
    """Get user's templates and public templates"""
    try:
        # Get user's templates
        user_response = supabase_client.get_client().table("templates").select("*").eq("user_id", current_user.id).execute()
        
        # Get public templates
        public_response = supabase_client.get_client().table("templates").select("*").eq("is_public", True).neq("user_id", current_user.id).execute()
        
        templates = []
        templates.extend([Template(**t) for t in user_response.data])
        templates.extend([Template(**t) for t in public_response.data])
        
        return templates
        
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch templates")

@router.get("/{template_id}", response_model=Template)
async def get_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific template"""
    try:
        response = supabase_client.get_client().table("templates").select("*").eq("id", template_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template = response.data[0]
        
        # Check if user can access template (owner or public)
        if template["user_id"] != current_user.id and not template["is_public"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return Template(**template)
        
    except Exception as e:
        logger.error(f"Error fetching template: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch template")

@router.put("/{template_id}", response_model=Template)
async def update_template(
    template_id: str,
    template_update: TemplateUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update template (only owner can update)"""
    try:
        # Check if template exists and belongs to user
        existing = supabase_client.get_client().table("templates").select("*").eq("id", template_id).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Update template
        update_data = template_update.dict(exclude_unset=True)
        response = supabase_client.get_client().table("templates").update(update_data).eq("id", template_id).eq("user_id", current_user.id).execute()
        
        return Template(**response.data[0])
        
    except Exception as e:
        logger.error(f"Error updating template: {e}")
        raise HTTPException(status_code=500, detail="Failed to update template")

@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete template (only owner can delete)"""
    try:
        # Check if template exists and belongs to user
        existing = supabase_client.get_client().table("templates").select("*").eq("id", template_id).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Delete template
        supabase_client.get_client().table("templates").delete().eq("id", template_id).eq("user_id", current_user.id).execute()
        
        return {"message": "Template deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting template: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete template")

@router.post("/{template_id}/use")
async def use_template(
    template_id: str,
    current_user: User = Depends(get_current_user)
):
    """Increment template usage count"""
    try:
        # Check if template exists and is accessible
        response = supabase_client.get_client().table("templates").select("*").eq("id", template_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template = response.data[0]
        
        # Check access (owner or public)
        if template["user_id"] != current_user.id and not template["is_public"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Increment usage count
        supabase_client.get_client().table("templates").update({"usage_count": template["usage_count"] + 1}).eq("id", template_id).execute()
        
        return {"message": "Template usage recorded"}
        
    except Exception as e:
        logger.error(f"Error recording template usage: {e}")
        raise HTTPException(status_code=500, detail="Failed to record template usage")
