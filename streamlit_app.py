import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Artistic Pencil Sketch Creator",
    page_icon="✏️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .stTitle {
            font-size: 3rem !important;
            color: #1E1E1E;
            text-align: center;
            padding-bottom: 2rem;
        }
        .upload-text {
            font-size: 1.2rem;
            color: #4A4A4A;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stAlert {
            background-color: #f0f2f6;
            border: none;
            border-radius: 10px;
        }
        .download-btn {
            text-align: center;
            padding: 1rem;
        }
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

def create_pencil_sketch(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert the grayscale image
    inverted_image = 255 - gray_image
    # Apply Gaussian blur to the inverted image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    # Invert the blurred image
    inverted_blurred = 255 - blurred
    # Create the pencil sketch
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    return pencil_sketch

# App header with emoji
st.markdown("# ✏️ Artistic Pencil Sketch Creator")
st.markdown("<p class='upload-text'>Transform your photos into beautiful pencil sketches</p>", unsafe_allow_html=True)

# Create three columns for better layout
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    # File uploader with custom styling
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpeg", "jpg", "png"],
        help="Upload a JPEG or PNG image to convert"
    )

if uploaded_file is not None:
    try:
        # Create columns for side-by-side comparison
        col1, col2 = st.columns(2)
        
        # Original image processing
        image = Image.open(uploaded_file)
        
        with col1:
            st.markdown("### Original Image")
            st.image(image, use_column_width=True)
        
        # Convert PIL Image to OpenCV format
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Generate the pencil sketch
        with st.spinner("Creating your sketch..."):
            pencil_sketch = create_pencil_sketch(image)
        
        with col2:
            st.markdown("### Pencil Sketch")
            st.image(pencil_sketch, use_column_width=True)
        
        # Centered download button with custom styling
        st.markdown("<div class='download-btn'>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Sketch",
            data=cv2.imencode('.png', np.array(pencil_sketch))[1].tobytes(),
            file_name="artistic_pencil_sketch.png",
            mime="image/png",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Oops! Something went wrong while processing your image. Please try again.")
        st.exception(e)

# Add footer with instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Click the 'Choose an image...' button above
    2. Select a JPEG or PNG image from your device
    3. Wait a moment for the sketch to be generated
    4. Click 'Download Sketch' to save your artwork
    
    For best results, use clear images with good contrast and lighting.
    """)
