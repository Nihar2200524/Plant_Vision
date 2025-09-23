// Perenual Plant API integration
const API_BASE_URL = 'https://perenual.com/api';
const API_KEY = 'YOUR_PERENUAL_API_KEY'; // Replace with your actual API key

export interface PlantApiResponse {
  data: PlantData[];
  to: number;
  per_page: number;
  current_page: number;
  from: number;
  last_page: number;
  total: number;
}

export interface PlantData {
  id: number;
  common_name: string;
  scientific_name: string[];
  other_name: string[];
  cycle?: string;
  watering?: string;
  sunlight?: string[];
  default_image?: {
    license?: number;
    license_name?: string;
    license_url?: string;
    original_url?: string;
    regular_url?: string;
    medium_url?: string;
    small_url?: string;
    thumbnail?: string;
  };
}

export const searchPlants = async (query: string): Promise<PlantData[]> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/species-list?key=${API_KEY}&q=${encodeURIComponent(query)}&page=1&per_page=10`
    );
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }
    
    const data: PlantApiResponse = await response.json();
    return data.data || [];
  } catch (error) {
    console.error('Error fetching plants:', error);
    
    // Return mock data as fallback for demo purposes
    return getMockPlantData(query);
  }
};

// Mock data fallback for when API is unavailable or rate-limited
const getMockPlantData = (query: string): PlantData[] => {
  const mockPlants: PlantData[] = [
    {
      id: 1,
      common_name: "Rose",
      scientific_name: ["Rosa rubiginosa"],
      other_name: ["Sweet Briar", "Eglantine"],
      watering: "Average",
      sunlight: ["Full sun", "Part shade"],
      default_image: {
        medium_url: "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
        original_url: "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800"
      }
    },
    {
      id: 2,
      common_name: "Monstera",
      scientific_name: ["Monstera deliciosa"],
      other_name: ["Swiss Cheese Plant", "Split-leaf Philodendron"],
      watering: "Average",
      sunlight: ["Part shade"],
      default_image: {
        medium_url: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        original_url: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"
      }
    },
    {
      id: 3,
      common_name: "Lavender",
      scientific_name: ["Lavandula angustifolia"],
      other_name: ["English Lavender", "True Lavender"],
      watering: "Minimum",
      sunlight: ["Full sun"],
      default_image: {
        medium_url: "https://images.unsplash.com/photo-1499002238440-d264edd596ec?w=400",
        original_url: "https://images.unsplash.com/photo-1499002238440-d264edd596ec?w=800"
      }
    }
  ];
  
  // Filter mock plants based on query
  return mockPlants.filter(plant => 
    plant.common_name.toLowerCase().includes(query.toLowerCase()) ||
    plant.scientific_name.some(name => name.toLowerCase().includes(query.toLowerCase())) ||
    plant.other_name.some(name => name.toLowerCase().includes(query.toLowerCase()))
  );
};