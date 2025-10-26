import { useState } from 'react'

interface SidebarProps {
  onCreateClick: () => void
}

export default function Sidebar({ onCreateClick }: SidebarProps) {
  const [folders] = useState<string[]>(['Documents', 'Research', 'Notes'])
  const [selectedFolder, setSelectedFolder] = useState<string>('Documents')

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <h2 className="text-lg font-semibold">Knowledge Base</h2>
      </div>

      {/* Folders */}
      <div className="flex-1 overflow-auto p-2">
        <div className="mb-4">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-3">
            Folders
          </h3>
          {folders.map((folder) => (
            <button
              key={folder}
              onClick={() => setSelectedFolder(folder)}
              className={`w-full px-3 py-2 text-left rounded-lg flex items-center hover:bg-gray-800 ${
                selectedFolder === folder ? 'bg-gray-800' : ''
              }`}
            >
              <svg
                className="w-4 h-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                />
              </svg>
              {folder}
            </button>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mb-4">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-3">
            Quick Actions
          </h3>
          <button
            onClick={onCreateClick}
            className="w-full px-3 py-2 text-left rounded-lg flex items-center hover:bg-gray-800 text-blue-400"
          >
            <svg
              className="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            Create Content
          </button>
          <button className="w-full px-3 py-2 text-left rounded-lg flex items-center hover:bg-gray-800">
            <svg
              className="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
              />
            </svg>
            Upload Document
          </button>
        </div>
      </div>
    </div>
  )
}
