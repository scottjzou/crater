import { useState } from 'react'

interface CreateContentModalProps {
  onClose: () => void
}

export default function CreateContentModal({ onClose }: CreateContentModalProps) {
  const [step, setStep] = useState(1)
  const [uploadMode, setUploadMode] = useState<'example' | 'template' | null>(null)

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-auto">
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
          {step === 1 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Choose creation method:</h3>
              <div className="space-y-4">
                <button
                  onClick={() => {
                    setUploadMode('example')
                    setStep(2)
                  }}
                  className="w-full p-6 border-2 border-gray-300 rounded-lg text-left hover:border-blue-500 hover:bg-blue-50 transition"
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg className="h-8 w-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <div className="ml-4">
                      <h4 className="text-lg font-semibold text-gray-900">Upload Example</h4>
                      <p className="text-sm text-gray-500">Upload your desired output format and we'll generate content matching it.</p>
                    </div>
                  </div>
                </button>

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
                      <p className="text-sm text-gray-500">Choose from our library of pre-built templates for quick content generation.</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">
                {uploadMode === 'example' ? 'Upload Example Document' : 'Select Knowledge Sources'}
              </h3>
              <p className="text-sm text-gray-500 mb-6">
                {uploadMode === 'example'
                  ? 'Upload a document that shows your desired output format'
                  : 'Select which documents to use as your knowledge base'}
              </p>
              <button
                onClick={() => setStep(1)}
                className="text-blue-600 hover:text-blue-800 mb-4"
              >
                ← Back
              </button>
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
          {step > 1 && (
            <button
              onClick={() => setStep(step + 1)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Next
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
