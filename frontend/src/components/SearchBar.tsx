import React, { useState, useRef } from 'react'
import { FiSearch, FiCamera, FiType, FiX } from 'react-icons/fi'

interface SearchBarProps {
  onTextSearch: (query: string) => void
  onImageSearch: (file: File) => void
  onClearSearch?: () => void
  searchMode: 'all' | 'text' | 'image'
}

const SearchBar: React.FC<SearchBarProps> = ({
  onTextSearch,
  onImageSearch,
  onClearSearch,
  searchMode,
}) => {
  const [query, setQuery] = useState('')
  const [localSearchMode, setLocalSearchMode] = useState<'text' | 'image'>(
    'text'
  )
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleTextSearch = (e: React.FormEvent) => {
    e.preventDefault()
    onTextSearch(query)
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onImageSearch(e.target.files[0])
    }
  }

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  return (
    <div className='w-full max-w-2xl mx-auto'>
      <div className='flex items-center gap-2 bg-white rounded-lg shadow-sm border border-gray-200 p-1'>
        <div className='flex rounded-md bg-gray-100 p-1'>
          <button
            type='button'
            onClick={() => setLocalSearchMode('text')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm ${
              localSearchMode === 'text'
                ? 'bg-white text-indigo-600 shadow-sm'
                : 'text-gray-600 hover:text-indigo-600'
            }`}
          >
            <FiType className='h-4 w-4' />
          </button>
          <button
            type='button'
            onClick={() => {
              setLocalSearchMode('image')
              triggerFileInput()
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm ${
              localSearchMode === 'image'
                ? 'bg-white text-indigo-600 shadow-sm'
                : 'text-gray-600 hover:text-indigo-600'
            }`}
          >
            <FiCamera className='h-4 w-4' />
          </button>
        </div>

        {localSearchMode === 'text' && (
          <form className='flex-1 flex' onSubmit={handleTextSearch}>
            <div className='relative flex-1'>
              <input
                type='text'
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder='Search products...'
                className='w-full pl-3 pr-10 py-2 text-sm text-gray-700 focus:outline-none'
              />
              <button
                type='submit'
                className='absolute right-0 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-indigo-600'
              >
                <FiSearch className='h-4 w-4' />
              </button>
            </div>
          </form>
        )}
        {localSearchMode === 'image' && (
          <div className='flex-1 flex items-center px-3 text-sm text-gray-500'>
            Click the camera icon to upload an image
          </div>
        )}

        {searchMode !== 'all' && onClearSearch && (
          <button
            onClick={() => {
              setQuery('')
              onClearSearch()
            }}
            className='px-3 py-1.5 text-gray-400 hover:text-indigo-600 border-l border-gray-200'
          >
            <FiX className='h-4 w-4' />
          </button>
        )}

        <input
          ref={fileInputRef}
          type='file'
          accept='image/*'
          onChange={handleImageUpload}
          className='hidden'
        />
      </div>
    </div>
  )
}

export default SearchBar
