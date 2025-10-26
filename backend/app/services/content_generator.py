import openai
from typing import List, Dict, Any, Optional
import logging
import tiktoken
from app.config import settings

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        try:
            response = await openai.Embedding.acreate(
                model=settings.embedding_model,
                input=texts
            )
            return [item["embedding"] for item in response["data"]]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    async def retrieve_relevant_chunks(
        self, 
        query: str, 
        chunks: List[Dict[str, Any]], 
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve most relevant chunks using semantic search"""
        try:
            # Generate query embedding
            query_embedding = await self.generate_embeddings([query])[0]
            
            # Calculate similarities (simplified - in production, use vector DB)
            similarities = []
            for chunk in chunks:
                if "embedding" in chunk:
                    # Calculate cosine similarity
                    similarity = self._cosine_similarity(query_embedding, chunk["embedding"])
                    similarities.append((similarity, chunk))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[0], reverse=True)
            return [chunk for _, chunk in similarities[:top_k]]
            
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {e}")
            raise
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    async def generate_content_preview(
        self,
        source_chunks: List[Dict[str, Any]],
        template_prompt: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        output_format: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate preview (ToC, style, example snippet)"""
        try:
            # Combine source chunks
            context = "\n\n".join([chunk["text"] for chunk in source_chunks])
            
            # Create preview prompt
            preview_prompt = f"""
            Based on the following source material, create a content generation plan:
            
            Source Material:
            {context[:4000]}  # Limit context for preview
            
            Please provide:
            1. A detailed table of contents with section descriptions
            2. A style guide (tone, audience level, format)
            3. A 200-word example snippet showing the writing style
            4. List the main source citations that will be referenced
            
            Format your response as JSON with keys: toc, style_guide, example_snippet, source_citations
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": preview_prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response (simplified - in production, use proper JSON parsing)
            content = response.choices[0].message.content
            
            return {
                "toc": {"sections": ["Introduction", "Main Content", "Conclusion"]},
                "style_guide": {"tone": "professional", "audience": "general"},
                "example_snippet": content[:200] + "...",
                "source_citations": [f"Document {i+1}" for i in range(len(source_chunks))],
                "estimated_tokens": self.count_tokens(context)
            }
            
        except Exception as e:
            logger.error(f"Error generating content preview: {e}")
            raise
    
    async def generate_full_content(
        self,
        source_chunks: List[Dict[str, Any]],
        template_prompt: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        toc: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate full content based on source chunks and requirements"""
        try:
            # Combine source chunks
            context = "\n\n".join([chunk["text"] for chunk in source_chunks])
            
            # Create generation prompt
            if custom_prompt:
                generation_prompt = f"""
                {custom_prompt}
                
                Source Material:
                {context}
                
                Please generate the requested content based on the source material above.
                """
            elif template_prompt:
                generation_prompt = f"""
                {template_prompt}
                
                Source Material:
                {context}
                
                Please generate content following the template above.
                """
            else:
                generation_prompt = f"""
                Based on the following source material, create comprehensive, well-structured content:
                
                Source Material:
                {context}
                
                Please create engaging, informative content that synthesizes the key information.
                """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": generation_prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating full content: {e}")
            raise
    
    async def refine_content(
        self,
        content: str,
        refinement_prompt: str
    ) -> str:
        """Refine existing content based on user feedback"""
        try:
            prompt = f"""
            Please refine the following content based on the user's request:
            
            User Request: {refinement_prompt}
            
            Current Content:
            {content}
            
            Please provide the refined version.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error refining content: {e}")
            raise

# Global instance
content_generator = ContentGenerator()
