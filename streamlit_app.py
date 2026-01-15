import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="PlantVision",
    page_icon="🌱",
    layout="wide"
)

# Constants
API_KEY = "sk-hpWB6968847d02ab614344"
API_BASE_URL = "https://perenual.com/api"

def search_plants(query):
    """Search for plants using the Perenual API"""
    if not query:
        return []
        
    try:
        url = f"{API_BASE_URL}/species-list"
        params = {
            "key": API_KEY,
            "q": query,
            "page": 1,
            "per_page": 12  # Fetch a few more to fill the grid
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Custom CSS for styling
st.markdown("""
    <style>
    .plant-card {
        background-color: #f0fdf4;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #bbf7d0;
        height: 100%;
    }
    .stButton>button {
        background-color: #4ade80;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #22c55e;
        border-color: #22c55e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🌱 PlantVision")
    st.markdown("<h3 style='text-align: center; color: #666;'>Discover the Nature Around You</h3>", unsafe_allow_html=True)

# Search Bar
query = st.text_input("Search for a plant...", placeholder="Try 'Rose', 'Monstera', or 'Lavender'")

# Search Logic
if query:
    with st.spinner("Searching for plants..."):
        plants = search_plants(query)
        
    if plants:
        st.success(f"Found {len(plants)} results for '{query}'")
        
        # Display results in a grid
        cols = st.columns(3)
        
        for idx, plant in enumerate(plants):
            col = cols[idx % 3]
            
            with col:
                # Get image URL or use fallback
                image_url = "https://images.unsplash.com/photo-1416879895648-5d6776113f03?w=800"
                if plant.get("default_image") and plant.get("default_image").get("regular_url"):
                    image_url = plant["default_image"]["regular_url"]
                elif plant.get("default_image") and plant.get("default_image").get("medium_url"):
                    image_url = plant["default_image"]["medium_url"]
                
                # Card content
                with st.container():
                    st.image(image_url, use_container_width=True)
                    st.subheader(plant.get("common_name", "Unknown Name"))
                    
                    scientific = plant.get("scientific_name", [])
                    if scientific:
                        st.markdown(f"**Scientific:** *{scientific[0]}*")
                    
                    # Some items might not have these details in the search list response
                    # Depending on API tier, detailed info requires ID lookup, 
                    # but we'll show what's available
                    if plant.get("watering"):
                        st.caption(f"💧 Watering: {plant['watering']}")
                    if plant.get("sunlight"):
                        st.caption(f"☀️ Sunlight: {', '.join(plant['sunlight'])}")
                        
                    st.markdown("---")

    else:
        st.warning("No plants found. Please try a different search term.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ using Streamlit & Perenual API</div>", 
    unsafe_allow_html=True
)
