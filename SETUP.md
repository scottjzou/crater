# Crater Setup Guide

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
Already configured with your API keys

**Frontend** (`frontend/.env`):
Already configured with your Supabase credentials

### 3. Set Up Supabase Database

Run these SQL commands in your Supabase SQL editor:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    folder_path TEXT,
    tags TEXT[],
    extracted_text TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create document_chunks table for embeddings
CREATE TABLE document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create generated_docs table
CREATE TABLE generated_docs (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    template_id TEXT,
    source_doc_ids TEXT[],
    toc JSONB,
    metadata JSONB,
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create templates table
CREATE TABLE templates (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    prompt_template TEXT NOT NULL,
    parameters JSONB DEFAULT '{}',
    is_public BOOLEAN DEFAULT FALSE,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_folder_path ON documents(folder_path);
CREATE INDEX idx_documents_tags ON documents USING GIN(tags);
CREATE INDEX idx_generated_docs_user_id ON generated_docs(user_id);
CREATE INDEX idx_templates_user_id ON templates(user_id);
```

### 4. Set Up Storage Bucket

In Supabase dashboard:
1. Go to Storage
2. Create new bucket named `documents`
3. Set it to public or configure RLS policies

### 5. Run the Application

**Backend** (Terminal 1):
```bash
cd backend
python -m app.main
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

### 6. Access the Application

Open your browser and go to:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Next Steps

1. **Configure RLS Policies** in Supabase for proper data security
2. **Get your Supabase Service Role Key** and add it to `backend/.env`
3. **Test the document upload** functionality
4. **Test the content generation** feature

## Troubleshooting

### Backend Issues
- Make sure Python 3.11+ is installed
- Check that all environment variables are set
- Verify Supabase connection

### Frontend Issues
- Run `npm install` again if packages are missing
- Check browser console for errors
- Verify environment variables in `.env`

### Database Issues
- Check Supabase connection
- Verify tables were created
- Check RLS policies
