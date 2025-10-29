import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { supabase } from './services/supabase'
import Sidebar from './components/Sidebar'
import DocumentViewer from './components/DocumentViewer'
import CreateContentModal from './components/CreateContentModal'
import Auth from './components/Auth'
import FileUpload from './components/FileUpload'
import './App.css'

function App() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [user, setUser] = useState<any>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [documents, setDocuments] = useState<any[]>([])

  useEffect(() => {
    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
    })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  useEffect(() => {
    if (user) {
      loadDocuments()
    }
  }, [user])

  const handleUploadComplete = async () => {
    setIsUploading(false)
    // Refresh documents list
    await loadDocuments()
  }

  const loadDocuments = async () => {
    try {
      const { data, error } = await supabase
        .from('documents')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (error) throw error
      setDocuments(data || [])
    } catch (error) {
      console.error('Error loading documents:', error)
    }
  }

  if (!user) {
    return <Auth />
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        onCreateClick={() => setIsCreateModalOpen(true)}
        onUploadClick={() => setIsUploading(true)}
      />
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Crater</h1>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Create Content
              </button>
              <button
                onClick={async () => {
                  await supabase.auth.signOut()
                }}
                className="px-4 py-2 text-gray-600 hover:text-gray-900"
              >
                Sign Out
              </button>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-auto">
          {isUploading ? (
            <div className="p-8">
              <FileUpload 
                onUploadComplete={handleUploadComplete}
              />
            </div>
          ) : (
            <DocumentViewer documents={documents} />
          )}
        </main>
      </div>
      {isCreateModalOpen && (
        <CreateContentModal 
          onClose={() => setIsCreateModalOpen(false)}
          documents={documents}
        />
      )}
    </div>
  )
}

export default App
