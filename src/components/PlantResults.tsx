import PlantCard from "./PlantCard";
import { Loader2 } from "lucide-react";

interface PlantData {
  id: number;
  common_name: string;
  scientific_name: string[];
  other_name: string[];
  watering?: string;
  sunlight?: string[];
  default_image?: {
    medium_url?: string;
    original_url?: string;
  };
}

interface PlantResultsProps {
  plants: PlantData[];
  isLoading: boolean;
  hasSearched: boolean;
}

const PlantResults = ({ plants, isLoading, hasSearched }: PlantResultsProps) => {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Searching for plants...</p>
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🌱</div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">
          Discover the Nature Around You
        </h2>
        <p className="text-muted-foreground max-w-md mx-auto">
          Enter a plant name above to explore detailed information about watering, 
          sunlight requirements, and more botanical details.
        </p>
      </div>
    );
  }

  if (plants.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🌸</div>
        <h2 className="text-xl font-semibold text-foreground mb-2">
          No plant found, try another name!
        </h2>
        <p className="text-muted-foreground">
          Try searching with different terms or check your spelling.
        </p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-foreground mb-2">
          {plants.length === 1 ? "Plant Found" : `${Math.min(plants.length, 3)} Plants Found`}
        </h2>
        <p className="text-muted-foreground">
          {plants.length > 3 
            ? "Showing top 3 matches for your search"
            : "Here's what we found for your search"
          }
        </p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
        {plants.slice(0, 3).map((plant) => (
          <PlantCard key={plant.id} plant={plant} />
        ))}
      </div>
    </div>
  );
};

export default PlantResults;