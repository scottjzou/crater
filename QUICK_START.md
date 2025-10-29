# Crater - Quick Start Guide

## What is Crater?

Crater is a knowledge management platform where you can:
- Upload and organize documents (PDFs, text files)
- Use AI to generate content from your documents
- Manage your knowledge base Obsidian-style

## Quick Setup (5 minutes)

### 1. Set Up Supabase Database

Go to your Supabase project: https://supabase.com/dashboard/project/jxbrkmlupznmiivvremi

**Step A: Run Schema SQL**
1. Go to SQL Editor
2. Open and run `supabase_schema.sql`
3. This creates all the tables

**Step B: Set Up Security**
1. Still in SQL Editor
2. Open and run `supabase_rls.sql`
3. This enables Row Level Security

**Step C: Create Storage**
1. Go to Storage
2. Create bucket named "documents"
3. Make it public (for now)

### 2. Configure Backend

```bash
cd backend
pip install -r requirements.txt
```

Copy your Supabase service role key from Project Settings → API and add it to `backend/.env`.

### 3. Configure Frontend

```bash
cd frontend
npm install
```

Frontend environment variables are already configured.

### 4. Run the Application

**Terminal 1 (Backend):**
```bash
cd backend
python -m app.main
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 5. Access the App

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## First Steps

1. **Sign Up** - Create an account
2. **Upload a PDF** - Click "Upload Document" in the sidebar
3. **Create Content** - Click "Create Content" and select your uploaded documents
4. **Generate** - Preview and generate AI-powered content

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (needs 3.11+)
- Make sure all dependencies installed: `pip install -r requirements.txt`
- Check `.env` file has correct API keys

**Frontend won't start:**
- Run `npm install` to install dependencies
- Check that port 5173 is available
- Look at browser console for errors

**Authentication issues:**
- Make sure Supabase Auth is enabled
- Check environment variables in `.env` files
- Try signing up again

**Upload fails:**
- Make sure storage bucket "documents" exists
- Check RLS policies are set up
- Verify file size is under 50MB

## Current Features

✅ User authentication
✅ Document upload (PDF, TXT, MD)
✅ Document viewing and organization
✅ AI-powered content generation from documents
✅ Template-based generation
✅ Secure storage with RLS policies

## Next Steps

The app is fully functional for the MVP. You can now:
- Upload multiple documents
- Generate content from them
- Manage your knowledge base

Future enhancements:
- Document editing
- Advanced templates
- Content marketplace
- Analytics dashboard

## Need Help?

Check out the detailed documentation:
- `SETUP_INSTRUCTIONS.md` - Comprehensive setup guide
- `IMPLEMENTATION_STATUS.md` - What's built
- `CURRENT_STATUS.md` - Current state

Or visit the GitHub repo: https://github.com/scottjzou/crater
