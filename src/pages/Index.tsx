import { useState } from "react";
import PlantSearch from "@/components/PlantSearch";
import PlantResults from "@/components/PlantResults";
import { searchPlants, PlantData } from "@/services/plantApi";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [plants, setPlants] = useState<PlantData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const { toast } = useToast();

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setHasSearched(true);
    
    try {
      const results = await searchPlants(query);
      setPlants(results);
      
      if (results.length === 0) {
        toast({
          title: "No plants found",
          description: `No results found for "${query}". Try a different search term.`,
        });
      }
    } catch (error) {
      console.error('Search error:', error);
      toast({
        title: "Search failed",
        description: "There was an error searching for plants. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="text-center py-12 px-4">
        <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
          🌱 PlantVision
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Discover the Nature Around You
        </p>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-12">
        <PlantSearch onSearch={handleSearch} isLoading={isLoading} />
        <PlantResults 
          plants={plants} 
          isLoading={isLoading} 
          hasSearched={hasSearched}
        />
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 backdrop-blur-sm mt-12">
        <div className="container mx-auto px-4 py-6 text-center">
          <p className="text-muted-foreground">
            Made with ❤️ using Perenual API & React
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
