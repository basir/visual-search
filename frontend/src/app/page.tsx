'use client'

import { useState, useEffect } from 'react'
import Header from '../components/Header'
import ProductGrid, { Product } from '../components/ProductGrid'
import Sidebar from '../components/Sidebar'
import { fetchProducts, searchByText, searchByImage } from '../services/api'

interface FilterOption {
  label: string
  value: string
  count: number
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([])
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [searchMode, setSearchMode] = useState<'all' | 'text' | 'image'>('all')
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [selectedColor, setSelectedColor] = useState<string>('')

  useEffect(() => {
    const loadProducts = async () => {
      setLoading(true)
      const data = await fetchProducts()
      setProducts(data)
      setFilteredProducts(data)
      setLoading(false)
    }

    loadProducts()
  }, [])

  useEffect(() => {
    let filtered = [...products]

    if (selectedCategory) {
      filtered = filtered.filter(
        (product) => product.category === selectedCategory
      )
    }

    if (selectedColor) {
      filtered = filtered.filter((product) => product.color === selectedColor)
    }

    setFilteredProducts(filtered)
  }, [products, selectedCategory, selectedColor])

  const handleTextSearch = async (query: string) => {
    setLoading(true)
    setSearchMode('text')
    setSelectedCategory('')
    setSelectedColor('')

    if (!query.trim()) {
      // If search is empty, show all products
      const data = await fetchProducts()
      setProducts(data)
      setSearchMode('all')
    } else {
      const results = await searchByText(query)
      setProducts(results)
    }

    setLoading(false)
  }

  const handleImageSearch = async (file: File) => {
    setLoading(true)
    setSearchMode('image')
    setSelectedCategory('')
    setSelectedColor('')

    const results = await searchByImage(file)
    setProducts(results)

    setLoading(false)
  }

  const handleClearSearch = async () => {
    setLoading(true)
    const data = await fetchProducts()
    setProducts(data)
    setSearchMode('all')
    setLoading(false)
  }

  const getCategories = (): FilterOption[] => {
    const categories = products.reduce((acc, product) => {
      if (product.category) {
        acc[product.category] = (acc[product.category] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    return Object.entries(categories).map(([value, count]) => ({
      label: value.charAt(0).toUpperCase() + value.slice(1),
      value,
      count,
    }))
  }

  const getColors = (): FilterOption[] => {
    // Filter products by category first if one is selected
    const filteredByCategory = selectedCategory
      ? products.filter((product) => product.category === selectedCategory)
      : products

    // Then get colors only from the filtered products
    const colors = filteredByCategory.reduce((acc, product) => {
      if (product.color) {
        acc[product.color] = (acc[product.color] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    return Object.entries(colors).map(([value, count]) => ({
      label: value.charAt(0).toUpperCase() + value.slice(1),
      value,
      count,
    }))
  }

  // Reset color selection when category changes
  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category)
    setSelectedColor('') // Reset color when category changes
  }

  return (
    <main className='min-h-screen bg-gradient-to-b from-gray-50 to-white'>
      <Header
        onTextSearch={handleTextSearch}
        onImageSearch={handleImageSearch}
        onClearSearch={handleClearSearch}
        searchMode={searchMode}
      />
      <div className='container mx-auto px-4 py-8'>
        <div className='flex gap-8'>
          <Sidebar
            categories={getCategories()}
            colors={getColors()}
            selectedCategory={selectedCategory}
            selectedColor={selectedColor}
            onCategoryChange={handleCategoryChange}
            onColorChange={setSelectedColor}
          />
          <div className='flex-1'>
            {loading ? (
              <div className='flex justify-center items-center py-20'>
                <div className='relative w-20 h-20'>
                  <div className='absolute top-0 left-0 w-full h-full border-4 border-indigo-200 rounded-full animate-ping'></div>
                  <div className='absolute top-0 left-0 w-full h-full border-4 border-t-indigo-500 rounded-full animate-spin'></div>
                </div>
              </div>
            ) : (
              <div>
                {/* {searchMode !== 'all' && (
                  <div className='text-center mb-8'>
                    <p className='text-gray-600'>
                      {searchMode === 'text'
                        ? 'Text search results'
                        : 'Visual search results'}
                    </p>
                  </div>
                )} */}
                <ProductGrid products={filteredProducts} />
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
