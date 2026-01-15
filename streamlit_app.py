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
            model="meta-llama/llama-4-scout-17b-16e-instruct",
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

# Custom CSS with "WOW" Design System
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #15803d; /* Green 700 */
        --primary-light: #dcfce7; /* Green 100 */
        --secondary: #f0fdf4; /* Green 50 */
        --accent: #22c55e; /* Green 500 */
        --background: #f8fafc; /* Slate 50 */
        --text-dark: #0f172a; /* Slate 900 */
        --text-muted: #64748b; /* Slate 500 */
        --card-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --hover-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --gradient-hero: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%);
        --gradient-card: linear-gradient(145deg, #ffffff, #f0fdf4);
    }

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* App Background */
    .stApp {
        background-color: var(--background);
        background-image: 
            radial-gradient(at 0% 0%, rgba(34, 197, 94, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(34, 197, 94, 0.1) 0px, transparent 50%);
    }

    /* Custom Header */
    .main-header {
        text-align: center; 
        padding: 4rem 0 2rem 0;
        background: linear-gradient(135deg, #166534 0%, #15803d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: var(--text-muted);
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Plant Cards */
    .plant-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: var(--card-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .plant-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
    }
    
    .plant-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--hover-shadow);
    }
    
    .plant-card img {
        border-radius: 12px;
        width: 100%;
        height: 220px;
        object-fit: cover;
        margin-bottom: 1rem;
        transition: transform 0.5s ease;
    }
    
    .plant-card:hover img {
        transform: scale(1.05);
    }
    
    .plant-card h3 {
        color: var(--text-dark);
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 1.25rem;
    }
    
    .plant-card .scientific {
        color: var(--primary);
        font-style: italic;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .plant-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }
    
    .plant-info span.icon {
        background: var(--primary-light);
        color: var(--primary);
        padding: 4px;
        border-radius: 6px;
        font-size: 1rem;
    }

    /* Streamlit Components Styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.2s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: 600;
        letter-spacing: 0.025em;
        box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.3);
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.4);
    }
    
    /* Input/Camera Container styles */
    .upload-container {
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.5);
    }
    
    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: var(--card-shadow);
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🌱 PlantVision</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Discover the beauty of nature with AI-powered identification</p>', unsafe_allow_html=True)

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
                            <img src="{image_url}" loading="lazy">
                            <h3>{plant.get("common_name", "Unknown")}</h3>
                            <span class="scientific">{plant.get("scientific_name", [""])[0]}</span>
                            <div class="plant-info">
                                <span class="icon">💧</span>
                                <span>{plant.get("watering", "Unknown")}</span>
                            </div>
                            <div class="plant-info">
                                <span class="icon">☀️</span>
                                <span>{', '.join(plant.get("sunlight", []))}</span>
                            </div>
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
                        <div class="plant-card">
                            <h2 style="color: #15803d; font-weight: 700; margin-bottom: 1rem;">{plant.get("common_name")}</h2>
                            <img src="{image_url}" style="height: 300px;">
                            <span class="scientific" style="font-size: 1.1rem; margin-bottom: 1.5rem;">{plant.get("scientific_name", [""])[0]}</span>
                            
                            <div style="background: #f0fdf4; padding: 1rem; border-radius: 12px; margin-top: 1rem;">
                                <div class="plant-info" style="font-size: 1rem; margin-bottom: 0.8rem;">
                                    <span class="icon" style="font-size: 1.2rem;">💧</span>
                                    <strong style="color: #0f172a; margin-left: 0.5rem;">Watering:</strong>
                                    <span style="margin-left: auto;">{plant.get("watering")}</span>
                                </div>
                                <div class="plant-info" style="font-size: 1rem;">
                                    <span class="icon" style="font-size: 1.2rem;">☀️</span>
                                    <strong style="color: #0f172a; margin-left: 0.5rem;">Sunlight:</strong>
                                    <span style="margin-left: auto;">{', '.join(plant.get("sunlight", []))}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(f"AI identified this as **{identified_name}**, but no detailed care info was found in our database.")
                # Error handled inside identify function
                

# Footer
st.markdown("---")
st.markdown("<center style='color:#888'>Built with Streamlit, Perenual API & Groq Vision AI</center>", unsafe_allow_html=True)
