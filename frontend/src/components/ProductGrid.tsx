/* eslint-disable @next/next/no-img-element */
import React from 'react'
import { motion } from 'framer-motion'
import Image from 'next/image'
export interface Product {
  id: number
  name: string
  price: number
  image_url: string
  category?: string
  color?: string
}

interface ProductGridProps {
  products: Product[]
}

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const item = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
}

const ProductGrid: React.FC<ProductGridProps> = ({ products }) => {
  return (
    <div className='container mx-auto px-4 py-8'>
      {products.length === 0 ? (
        <div className='text-center py-10'>
          <p className='text-gray-500 text-xl'>No products found</p>
        </div>
      ) : (
        <motion.div
          key={products.map((p) => p.id).join(',')}
          variants={container}
          initial='hidden'
          animate='show'
          className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6'
        >
          {products.map((product) => (
            <motion.div
              variants={item}
              key={product.id}
              className='bg-white rounded-xl shadow-sm hover:shadow-xl hover:scale-102 transition-all duration-300 overflow-hidden w-full'
            >
              <div className='relative h-64 w-full overflow-hidden'>
                <Image
                  src={product.image_url}
                  alt={product.name}
                  fill
                  className='object-cover object-center w-full h-full'
                  sizes='(max-width: 640px) 100vw, (max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw'
                />
              </div>
              <div className='p-4'>
                <h3 className='text-lg font-medium text-gray-900 hover:text-indigo-600 transition-colors duration-300'>
                  {product.name}
                </h3>
                <div className='mt-2 flex items-center justify-between'>
                  <p className='text-xl font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'>
                    ${product.price.toFixed(2)}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  )
}

export default ProductGrid
