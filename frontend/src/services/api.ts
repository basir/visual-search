import { Product } from '../components/ProductGrid';

const API_URL = 'http://localhost:8000';

export const fetchProducts = async (): Promise<Product[]> => {
  try {
    const response = await fetch(`${API_URL}/api/products`);
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

export const searchByText = async (query: string): Promise<Product[]> => {
  try {
    const response = await fetch(`${API_URL}/api/search/text?query=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error('Failed to search products');
    }
    return await response.json();
  } catch (error) {
    console.error('Error searching products:', error);
    return [];
  }
};

export const searchByImage = async (file: File): Promise<Product[]> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/api/search/image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to search by image');
    }

    return await response.json();
  } catch (error) {
    console.error('Error searching by image:', error);
    return [];
  }
}; 