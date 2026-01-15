import streamlit as st
import requests
import time

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
            "per_page": 12
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Custom CSS
st.markdown("""
    <style>
    .plant-card {
        background-color: #f0fdf4;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #bbf7d0;
        height: 100%;
        transition: transform 0.2s;
    }
    .plant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4ade80;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #22c55e;
        border-color: #22c55e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.title("🌱 PlantVision")
st.markdown("<h3 style='color: #666;'>Discover the Nature Around You</h3>", unsafe_allow_html=True)

# Tabs for different modes
tab1, tab2 = st.tabs(["🔍 Search by Name", "📸 Identify by Image"])

# --- TAB 1: SEARCH ---
with tab1:
    st.markdown("#### Search the Database")
    query = st.text_input("Enter plant name", placeholder="Try 'Rose', 'Monstera', or 'Lavender'", label_visibility="collapsed")

    if query:
        with st.spinner("Searching database..."):
            plants = search_plants(query)
            
        if plants:
            st.success(f"Found {len(plants)} results for '{query}'")
            
            cols = st.columns(3)
            for idx, plant in enumerate(plants):
                col = cols[idx % 3]
                with col:
                    # Logic to find best image
                    image_url = "https://images.unsplash.com/photo-1416879895648-5d6776113f03?w=800"
                    if plant.get("default_image") and plant.get("default_image").get("regular_url"):
                        image_url = plant["default_image"]["regular_url"]
                    elif plant.get("default_image") and plant.get("default_image").get("medium_url"):
                        image_url = plant["default_image"]["medium_url"]
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="plant-card">
                            <img src="{image_url}" style="width:100%; border-radius:10px; height:200px; object-fit:cover; margin-bottom:10px;">
                            <h3>{plant.get("common_name", "Unknown")}</h3>
                            <p><i>{plant.get("scientific_name", [""])[0]}</i></p>
                            <p>💧 {plant.get("watering", "Unknown")}</p>
                            <p>☀️ {', '.join(plant.get("sunlight", []))}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("No plants found. Please try a different search term.")

# --- TAB 2: IDENTIFY ---
with tab2:
    st.markdown("#### 📸 Snap & Identify")
    st.info("Upload a photo or use your camera to identify a plant.")
    
    col_input, col_preview = st.columns([1, 1])
    
    with col_input:
        input_type = st.radio("Select Input Method", ["Upload Image", "Use Camera"], horizontal=True)
        
        image_file = None
        if input_type == "Upload Image":
            image_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
        else:
            image_file = st.camera_input("Take a photo")

    # Preview and Analyze
    if image_file:
        with col_preview:
            st.image(image_file, caption="Input Image", width=300)
            
        st.divider()
        
        if st.button("🔍 Identify Plant"):
            with st.spinner("Analyzing image features..."):
                time.sleep(2) # Simulate processing time
                
                # NOTE: Real image identification requires a generic Vision API (like Gemini/OpenAI) 
                # or a specific Plant ID API. The basic Perenual key is for DB search.
                # For this demo, we simulate a successful identification.
                
                st.success("Analysis Complete!")
                st.balloons()
                
                # Simulated result
                simulated_match = "Sunflower"
                confidence = "98.5%"
                
                st.markdown(f"""
                ### 🎯 Match Found: **{simulated_match}**
                **Confidence:** {confidence}
                
                *Note: This is a simulated result for demonstration. Connect a Vision API for real-time analysis.*
                """)
                
                # Fetch details for the "identified" plant
                details = search_plants(simulated_match)
                if details:
                    plant = details[0]
                    st.json(plant, expanded=False)
                    
                    image_url = "https://images.unsplash.com/photo-1416879895648-5d6776113f03?w=800"
                    if plant.get("default_image") and plant.get("default_image").get("regular_url"):
                        image_url = plant["default_image"]["regular_url"]
                        
                    st.markdown(f"""
                    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 10px; border: 1px solid #4ade80;">
                        <h2>{plant.get("common_name")}</h2>
                        <img src="{image_url}" style="width: 100%; max-width: 400px; border-radius: 10px;">
                        <p><strong>Scientific Name:</strong> {plant.get("scientific_name", [""])[0]}</p>
                        <p><strong>Watering:</strong> {plant.get("watering")}</p>
                        <p><strong>Sunlight:</strong> {', '.join(plant.get("sunlight", []))}</p>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center style='color:#888'>Built with Streamlit & Perenual API</center>", unsafe_allow_html=True)
