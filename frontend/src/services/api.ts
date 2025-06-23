import axios from 'axios';

// Define the structure of our Product object for TypeScript
export interface Product {
  product_id: number;
  product_name: string;
  category: string;
  price: number;
  image_url: string;
  earth_score: number;
  // Add other fields if you need them in the UI
}

// Create an axios instance with a base URL.
// This means we don't have to type 'http://localhost:8000' for every request.
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Export functions for each of our API endpoints
export const getAllProducts = async (): Promise<Product[]> => {
  const response = await apiClient.get('/api/products');
  return response.data;
};

export const getProductById = async (id: number): Promise<Product> => {
  const response = await apiClient.get(`/api/products/${id}`);
  return response.data;
};

export const getRecommendations = async (id: number): Promise<Product[]> => {
  const response = await apiClient.get(`/api/products/${id}/recommendations`);
  return response.data;
};