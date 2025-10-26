export default function DocumentViewer() {
  return (
    <div className="flex items-center justify-center h-full p-12">
      <div className="text-center">
        <svg
          className="mx-auto h-24 w-24 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 className="mt-6 text-lg font-medium text-gray-900">Welcome to Crater</h3>
        <p className="mt-2 text-sm text-gray-500">
          Upload documents to get started, or create content from your knowledge base.
        </p>
      </div>
    </div>
  )
}
