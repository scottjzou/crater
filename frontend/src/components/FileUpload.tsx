import { useState, useCallback } from 'react'
import axios from 'axios'

interface FileUploadProps {
  onUploadComplete: () => void
  folderPath?: string
}

export default function FileUpload({ onUploadComplete, folderPath }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    await uploadFiles(files)
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      await uploadFiles(files)
    }
  }

  const uploadFiles = async (files: File[]) => {
    setUploading(true)
    setProgress(0)

    for (const file of files) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('title', file.name)
        if (folderPath) {
          formData.append('folder_path', folderPath)
        }

        const response = await axios.post('/api/documents/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              )
              setProgress(percentCompleted)
            }
          },
        })

        setProgress(100)
        await new Promise((resolve) => setTimeout(resolve, 500))
      } catch (error) {
        console.error('Upload error:', error)
      }
    }

    setUploading(false)
    setProgress(0)
    onUploadComplete()
  }

  if (uploading) {
    return (
      <div className="p-6 border-2 border-dashed border-blue-500 rounded-lg bg-blue-50">
        <div className="flex items-center justify-center space-x-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <div>
            <p className="text-sm font-medium text-gray-700">Uploading...</p>
            <progress value={progress} max="100" className="w-full mt-2" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`p-6 border-2 border-dashed rounded-lg transition-colors ${
        isDragging
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <div className="text-center">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">
          Drag and drop files
        </h3>
        <p className="mt-2 text-sm text-gray-500">
          or{' '}
          <label className="text-blue-600 hover:text-blue-800 cursor-pointer">
            browse
            <input
              type="file"
              className="hidden"
              multiple
              accept=".pdf,.txt,.md,.docx"
              onChange={handleFileSelect}
            />
          </label>{' '}
          to upload
        </p>
        <p className="mt-2 text-xs text-gray-400">
          PDF, TXT, MD, or DOCX files
        </p>
      </div>
    </div>
  )
}
