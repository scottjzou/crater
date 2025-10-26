import PyPDF2
import pdfplumber
from typing import List, Dict, Any
import logging
import io

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    async def extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """Extract text from PDF using multiple methods for better accuracy"""
        try:
            # Try pdfplumber first (better for complex layouts)
            text = await self._extract_with_pdfplumber(pdf_data)
            if text.strip():
                return text
            
            # Fallback to PyPDF2
            text = await self._extract_with_pypdf2(pdf_data)
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    async def _extract_with_pdfplumber(self, pdf_data: bytes) -> str:
        """Extract text using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        return text
    
    async def _extract_with_pypdf2(self, pdf_data: bytes) -> str:
        """Extract text using PyPDF2"""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
        return text
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks for embedding"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "index": len(chunks),
                "start_word": i,
                "end_word": min(i + self.chunk_size, len(words)),
                "metadata": {
                    "chunk_size": len(chunk_words),
                    "total_words": len(words)
                }
            })
        
        return chunks
    
    async def process_pdf(self, pdf_data: bytes) -> Dict[str, Any]:
        """Complete PDF processing pipeline"""
        try:
            # Extract text
            text = await self.extract_text_from_pdf(pdf_data)
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            return {
                "text": text,
                "chunks": chunks,
                "word_count": len(text.split()),
                "chunk_count": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise

# Global instance
pdf_processor = PDFProcessor()
