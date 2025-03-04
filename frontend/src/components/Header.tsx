import React from 'react'
import Link from 'next/link'
import SearchBar from './SearchBar'
import { FiShoppingCart, FiUser } from 'react-icons/fi'

interface HeaderProps {
  onTextSearch: (query: string) => void
  onImageSearch: (file: File) => void
  onClearSearch?: () => void
  searchMode: 'all' | 'text' | 'image'
}

const Header: React.FC<HeaderProps> = ({
  onTextSearch,
  onImageSearch,
  onClearSearch,
  searchMode,
}) => {
  return (
    <header className='bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50'>
      <div className='container mx-auto px-4 py-3'>
        <div className='flex justify-between gap-4'>
          <div>
            <Link
              href='/'
              className='text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'
            >
              Fashion Finder
            </Link>
          </div>

          <div className='flex-1 max-w-xl'>
            <SearchBar
              onTextSearch={onTextSearch}
              onImageSearch={onImageSearch}
              onClearSearch={onClearSearch}
              searchMode={searchMode}
            />
          </div>

          <div className='flex items-center gap-2'>
            <div className='flex items-center gap-1 pl-2'>
              <button className='relative p-2 text-gray-600 hover:text-indigo-600 transition-colors'>
                <FiShoppingCart className='w-5 h-5' />
                <span className='absolute -top-1 -right-1 w-4 h-4 text-xs bg-indigo-600 text-white rounded-full flex items-center justify-center'>
                  0
                </span>
              </button>

              <button className='p-2 text-gray-600 hover:text-indigo-600 transition-colors flex items-center gap-2'>
                <FiUser className='w-5 h-5' />
                <span className='text-sm hidden sm:inline'>Login</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
