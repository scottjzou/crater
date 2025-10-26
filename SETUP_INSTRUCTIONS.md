# Crater Setup Instructions

## Step 1: Install Dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Step 2: Set Up Supabase Database

Go to your Supabase project dashboard (https://supabase.com/dashboard/project/jxbrkmlupznmiivvremi)

### 2.1 Run Schema SQL
1. Go to SQL Editor
2. Copy and paste the contents of `supabase_schema.sql`
3. Click "Run" to create all tables

### 2.2 Set Up RLS Policies
1. Still in SQL Editor
2. Copy and paste the contents of `supabase_rls.sql`
3. Click "Run" to enable Row Level Security

### 2.3 Create Storage Bucket
1. Go to Storage in Supabase dashboard
2. Click "New bucket"
3. Name: `documents`
4. Make it **public** (for now - you can secure it later)
5. Click "Create bucket"

## Step 3: Get Service Role Key

1. Go to Project Settings → API
2. Copy the "service_role" key (keep this secret!)
3. Add it to `backend/.env` as `SUPABASE_SERVICE_ROLE_KEY`

## Step 4: Run the Application

### Start Backend (Terminal 1)
```bash
cd backend
python -m app.main
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

## Step 5: Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing the Application

1. The app will load at http://localhost:5173
2. Click "Create Content" to see the modal
3. You'll need to set up authentication first (Supabase Auth)

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Install dependencies: `pip install -r requirements.txt`
- Check .env file has all required keys

### Frontend won't start
- Run `npm install` again
- Check that port 5173 is not in use
- Check browser console for errors

### Database errors
- Verify all SQL was run successfully
- Check Supabase connection in dashboard
- Verify storage bucket was created

### Authentication issues
- Make sure Supabase Auth is enabled in project settings
- Check API keys in .env files are correct
