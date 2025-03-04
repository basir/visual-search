import React from 'react'

interface FilterOption {
  label: string
  value: string
  count: number
}

interface SidebarProps {
  categories: FilterOption[]
  colors: FilterOption[]
  selectedCategory: string
  selectedColor: string
  onCategoryChange: (category: string) => void
  onColorChange: (color: string) => void
}

const Sidebar: React.FC<SidebarProps> = ({
  categories,
  colors,
  selectedCategory,
  selectedColor,
  onCategoryChange,
  onColorChange,
}) => {
  return (
    <div className='w-64 bg-white shadow-lg rounded-lg p-6 space-y-6'>
      <div>
        <h3 className='text-lg font-semibold text-gray-800 mb-4'>Categories</h3>
        <div className='space-y-2'>
          <button
            onClick={() => onCategoryChange('')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm ${
              selectedCategory === ''
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span>All Categories</span>
          </button>
          {categories.map((category) => (
            <button
              key={category.value}
              onClick={() => onCategoryChange(category.value)}
              className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                selectedCategory === category.value
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <span>{category.label}</span>
              <span className='float-right text-xs text-gray-400'>
                ({category.count})
              </span>
            </button>
          ))}
        </div>
      </div>

      <div>
        <h3 className='text-lg font-semibold text-gray-800 mb-4'>Colors</h3>
        <div className='space-y-2'>
          <button
            onClick={() => onColorChange('')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm ${
              selectedColor === ''
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <div className='flex items-center'>
              <span>All Colors</span>
            </div>
          </button>
          {colors.map((color) => (
            <button
              key={color.value}
              onClick={() => onColorChange(color.value)}
              className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                selectedColor === color.value
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <div className='flex items-center'>
                <div
                  className='w-4 h-4 rounded-full mr-2'
                  style={{
                    backgroundColor: color.value.toLowerCase(),
                    border:
                      color.value.toLowerCase() === 'white'
                        ? '1px solid #e5e7eb'
                        : 'none',
                  }}
                />
                <span>{color.label}</span>
                <span className='ml-auto text-xs text-gray-400'>
                  ({color.count})
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Sidebar
