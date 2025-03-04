# Visual Search Frontend

This is the frontend for the AI-powered visual search e-commerce platform. It provides a user interface for browsing products, searching by text, and searching by image.

## Features

- Product browsing
- Text-based search
- Image-based visual search
- Responsive design

## Setup

1. Install dependencies:
```
npm install
```

2. Run the development server:
```
npm run dev
```

The frontend will run at http://localhost:3000

## Usage

- **Browse Products**: View all products on the home page
- **Text Search**: Enter keywords in the search bar and click "Search"
- **Visual Search**: Click the camera icon to upload an image and find visually similar products

## Project Structure

- `src/components/`: React components
  - `Header.tsx`: Navigation header
  - `SearchBar.tsx`: Search input with text and image upload
  - `ProductGrid.tsx`: Grid display of products
- `src/services/`: API services
  - `api.ts`: Functions for communicating with the backend
- `src/app/`: Next.js app router pages

## Technologies Used

- Next.js
- React
- TypeScript
- Tailwind CSS
