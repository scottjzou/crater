import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import DocumentViewer from './components/DocumentViewer'
import CreateContentModal from './components/CreateContentModal'
import './App.css'

function App() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar onCreateClick={() => setIsCreateModalOpen(true)} />
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Crater</h1>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Create Content
            </button>
          </div>
        </header>
        <main className="flex-1 overflow-auto">
          <DocumentViewer />
        </main>
      </div>
      {isCreateModalOpen && (
        <CreateContentModal onClose={() => setIsCreateModalOpen(false)} />
      )}
    </div>
  )
}

export default App
