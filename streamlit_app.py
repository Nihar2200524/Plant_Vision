import streamlit as st
import requests
import time
import base64
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="PlantVision",
    page_icon="🌱",
    layout="wide"
)

# Constants - Keys should be in .streamlit/secrets.toml or Streamlit Cloud Secrets
try:
    PERENUAL_API_KEY = st.secrets["PERENUAL_API_KEY"]
except:
    PERENUAL_API_KEY = "sk-hpWB6968847d02ab614344" # Fallback/Demo Key

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = "" # Placeholder - Needs to be set in secrets

PERENUAL_BASE_URL = "https://perenual.com/api"

def search_plants(query):
    """Search for plants using the Perenual API"""
    if not query:
        return []
        
    try:
        url = f"{PERENUAL_BASE_URL}/species-list"
        params = {
            "key": PERENUAL_API_KEY,
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

def identify_plant_with_groq(image_bytes):
    """Identify plant from image using Groq Vision model"""
    if not GROQ_API_KEY:
        st.error("Groq API Key is missing! Please configure it in Streamlit Secrets.")
        return None
        
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Encode image to base64
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Call Vision Model
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Identify this plant. Return ONLY the common name of the plant. Do not include sentences, just the name."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Vision API Error: {e}")
        return None

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
            with st.spinner("Analyzing image with AI..."):
                # Get bytes from the upload/camera buffer
                image_bytes = image_file.getvalue()
                
                # Real identification call using Groq
                identified_name = identify_plant_with_groq(image_bytes)
                
                if identified_name:
                    st.success("Analysis Complete!")
                    st.balloons()
                    
                    st.markdown(f"### 🎯 Match Found: **{identified_name}**")
                    
                    # Search for specific details in the Perenual Database using the identified name
                    with st.spinner(f"Fetching details for {identified_name}..."):
                        details = search_plants(identified_name)
                    
                    if details:
                        # Try to find an exact match if possible, otherwise take the first
                        plant = details[0]
                        
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
                    else:
                        st.info(f"AI identified this as **{identified_name}**, but no detailed care info was found in our database.")
                # Error handled inside identify function
                

# Footer
st.markdown("---")
st.markdown("<center style='color:#888'>Built with Streamlit, Perenual API & Groq Vision AI</center>", unsafe_allow_html=True)
