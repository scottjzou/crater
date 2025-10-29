import { useState, useEffect } from 'react'
import axios from 'axios'
import { supabase } from '../services/supabase'

interface CreateContentModalProps {
  onClose: () => void
  documents?: any[]
}

export default function CreateContentModal({ onClose, documents = [] }: CreateContentModalProps) {
  const [step, setStep] = useState(1)
  const [uploadMode, setUploadMode] = useState<'example' | 'template' | null>(null)
  const [selectedDocs, setSelectedDocs] = useState<string[]>([])
  const [preview, setPreview] = useState<any>(null)
  const [generating, setGenerating] = useState(false)

  const handleDocumentToggle = (docId: string) => {
    setSelectedDocs(prev =>
      prev.includes(docId)
        ? prev.filter(id => id !== docId)
        : [...prev, docId]
    )
  }

  const handleGeneratePreview = async () => {
    if (selectedDocs.length === 0) return
    
    setGenerating(true)
    try {
      const response = await axios.post('/api/content/generate/preview', {
        source_doc_ids: selectedDocs,
        custom_prompt: 'Generate a comprehensive content structure based on these documents',
      })
      setPreview(response.data)
      setStep(3)
    } catch (error) {
      console.error('Error generating preview:', error)
    } finally {
      setGenerating(false)
    }
  }

  const handleGenerateContent = async () => {
    setGenerating(true)
    try {
      const response = await axios.post('/api/content/generate', {
        source_doc_ids: selectedDocs,
        custom_prompt: 'Generate comprehensive content based on these documents',
      })
      onClose()
      // Could show success message
    } catch (error) {
      console.error('Error generating content:', error)
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">Create Content</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Step 1: Choose Method */}
          {step === 1 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Choose creation method:</h3>
              <div className="space-y-4">
                <button
                  onClick={() => {
                    setUploadMode('template')
                    setStep(2)
                  }}
                  className="w-full p-6 border-2 border-gray-300 rounded-lg text-left hover:border-blue-500 hover:bg-blue-50 transition"
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg className="h-8 w-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg font-semibold text-gray-900">Use Template</h4>
                      <p className="text-sm text-gray-500">Generate content from your documents using templates.</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Select Documents */}
          {step === 2 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Select Knowledge Sources</h3>
              <p className="text-sm text-gray-500 mb-6">
                Choose which documents to use as your knowledge base
              </p>
              
              <div className="space-y-2 max-h-96 overflow-y-auto mb-6">
                {documents.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">
                    No documents available. Please upload documents first.
                  </p>
                ) : (
                  documents.map((doc) => (
                    <label
                      key={doc.id}
                      className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={selectedDocs.includes(doc.id)}
                        onChange={() => handleDocumentToggle(doc.id)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                      <div className="ml-4 flex-1">
                        <p className="text-sm font-medium text-gray-900">{doc.title}</p>
                        <p className="text-xs text-gray-500 capitalize">{doc.file_type}</p>
                      </div>
                    </label>
                  ))
                )}
              </div>

              <div className="flex justify-between">
                <button
                  onClick={() => setStep(1)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  ← Back
                </button>
                <button
                  onClick={handleGeneratePreview}
                  disabled={selectedDocs.length === 0 || generating}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {generating ? 'Generating...' : 'Generate Preview'}
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Preview */}
          {step === 3 && preview && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Content Preview</h3>
              
              <div className="space-y-4 mb-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Example Snippet</h4>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {preview.example_snippet || 'No preview available'}
                  </p>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Estimated Tokens</h4>
                  <p className="text-sm text-gray-700">{preview.estimated_tokens || 'N/A'}</p>
                </div>
              </div>

              <div className="flex justify-between">
                <button
                  onClick={() => setStep(2)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  ← Back
                </button>
                <button
                  onClick={handleGenerateContent}
                  disabled={generating}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {generating ? 'Generating...' : 'Generate Full Content'}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}