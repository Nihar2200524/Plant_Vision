import { useState } from "react";
import { Droplets, Sun, ChevronDown, ChevronUp, ZoomIn } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";

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

interface PlantCardProps {
  plant: PlantData;
}

const PlantCard = ({ plant }: PlantCardProps) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const getWateringColor = (watering: string) => {
    switch (watering?.toLowerCase()) {
      case 'frequent': return 'bg-blue-100 text-blue-800';
      case 'average': return 'bg-green-100 text-green-800';
      case 'minimum': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getSunlightColor = (sunlight: string) => {
    switch (sunlight?.toLowerCase()) {
      case 'full sun': return 'bg-orange-100 text-orange-800';
      case 'part shade': return 'bg-amber-100 text-amber-800';
      case 'full shade': return 'bg-purple-100 text-purple-800';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  return (
    <Card className="plant-card fade-in overflow-hidden border-0 rounded-2xl">
      <CardHeader className="p-0">
        {plant.default_image?.medium_url ? (
          <Dialog>
            <DialogTrigger asChild>
              <div className="relative cursor-pointer group overflow-hidden rounded-t-2xl">
                <img
                  src={plant.default_image.medium_url}
                  alt={plant.common_name}
                  className="plant-image w-full h-48 object-cover"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <ZoomIn className="h-8 w-8 text-white" />
                </div>
              </div>
            </DialogTrigger>
            <DialogContent className="max-w-4xl">
              <img
                src={plant.default_image.original_url || plant.default_image.medium_url}
                alt={plant.common_name}
                className="w-full h-auto rounded-lg"
              />
            </DialogContent>
          </Dialog>
        ) : (
          <div className="h-48 bg-gradient-to-br from-primary-light to-accent flex items-center justify-center rounded-t-2xl">
            <span className="text-4xl">🌿</span>
          </div>
        )}
      </CardHeader>
      
      <CardContent className="p-6">
        <div className="space-y-4">
          <div>
            <h3 className="text-xl font-semibold text-foreground capitalize">
              {plant.common_name}
            </h3>
            {plant.scientific_name?.[0] && (
              <p className="text-muted-foreground italic text-sm mt-1">
                {plant.scientific_name[0]}
              </p>
            )}
          </div>

          {/* Care Information */}
          <div className="flex flex-wrap gap-2">
            {plant.watering && (
              <Badge variant="outline" className={`flex items-center gap-1 ${getWateringColor(plant.watering)}`}>
                <Droplets className="h-3 w-3" />
                {plant.watering} watering
              </Badge>
            )}
            {plant.sunlight?.[0] && (
              <Badge variant="outline" className={`flex items-center gap-1 ${getSunlightColor(plant.sunlight[0])}`}>
                <Sun className="h-3 w-3" />
                {plant.sunlight[0]}
              </Badge>
            )}
          </div>

          {/* Collapsible Extra Details */}
          {(plant.other_name?.length > 0 || plant.sunlight?.length > 1) && (
            <Collapsible open={isOpen} onOpenChange={setIsOpen}>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" className="w-full justify-between p-0 h-auto">
                  <span className="text-sm text-muted-foreground">More details</span>
                  {isOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent className="space-y-3 pt-3">
                {plant.other_name?.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-foreground mb-1">Other names:</h4>
                    <p className="text-sm text-muted-foreground">
                      {plant.other_name.slice(0, 3).join(", ")}
                      {plant.other_name.length > 3 && "..."}
                    </p>
                  </div>
                )}
                {plant.sunlight && plant.sunlight.length > 1 && (
                  <div>
                    <h4 className="text-sm font-medium text-foreground mb-2">All sunlight requirements:</h4>
                    <div className="flex flex-wrap gap-1">
                      {plant.sunlight.map((light, index) => (
                        <Badge 
                          key={index} 
                          variant="outline" 
                          className={`text-xs ${getSunlightColor(light)}`}
                        >
                          {light}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CollapsibleContent>
            </Collapsible>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default PlantCard;