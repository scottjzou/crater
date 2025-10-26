# Crater

Knowledge Management + RAG-Powered Content Creation Platform

An Obsidian-style knowledge management system where creators organize their source materials (PDFs, notes, documents) and use RAG (Retrieval-Augmented Generation) to create custom-formatted content from their knowledge base.

## Features

### Core Functionality
- **Obsidian-Style File Management**: Complete file organization with folders, tags, and linking
- **PDF Processing**: Extract and chunk text from PDF documents
- **RAG-Powered Generation**: Create content using semantic search across your knowledge base
- **Template Library**: Choose from pre-built templates or create your own
- **Content Refinement**: Iteratively improve generated content with chat interface

### Planned Features
- Real-time collaboration
- Marketplace integration
- Audio and video content generation
- Advanced graph visualization

## Tech Stack

**Backend:**
- FastAPI (Python)
- Supabase (PostgreSQL + Auth + Storage)
- OpenAI API (GPT-4 + Embeddings)
- pgvector for semantic search

**Frontend:**
- React + TypeScript
- Tailwind CSS
- Vite
- React Router

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI API key

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your credentials

# Run the server
python -m app.main
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Project Structure

```
crater/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py             # Configuration
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── services/
│   │   │   ├── supabase_client.py
│   │   │   ├── pdf_processor.py
│   │   │   └── content_generator.py
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── documents.py
│   │       ├── content.py
│   │       └── templates.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## Development

### Backend API Endpoints

- `GET /` - Health check
- `GET /health` - Health check with details
- `POST /api/auth/login` - User authentication
- `GET /api/documents/` - List documents
- `POST /api/documents/upload` - Upload document
- `POST /api/content/generate` - Generate content
- `GET /api/templates/` - List templates

### Database Schema

The application uses Supabase PostgreSQL with the following main tables:
- `documents` - Source documents and metadata
- `document_chunks` - Text chunks for vector search
- `generated_docs` - Generated content
- `templates` - Content generation templates
- `users` - User accounts

## License

MIT