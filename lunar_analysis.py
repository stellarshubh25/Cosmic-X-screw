import streamlit as st
import rasterio
import numpy as np
from PIL import Image
import rasterio.enums

st.title("Cosmic X Crew - Lunar Analysis")

# Your Dropbox link
DIRECT_URL = "https://www.dropbox.com/scl/fi/ilu80zbhluyluq6pcd516/ICY_CRATERS_SP.tif?rlkey=g2jqntrpris2lydo3i8qdx22g&st=g5mumz31&dl=1"

try:
    # 1. Connect to the cloud file
    with rasterio.open(DIRECT_URL) as src:
        st.write("Successfully connected to the map data!")
        
        # 2. Read and downsample to avoid crashing the server
        data = src.read(1, out_shape=(1, 1000, 1000), resampling=rasterio.enums.Resampling.bilinear)
        
        # 3. Normalize data (0-255) so the screen can show it
        data_norm = (255 * (data - np.min(data)) / (np.max(data) - np.min(data))).astype(np.uint8)
        
        # 4. Convert to image and display
        img = Image.fromarray(data_norm[0])
        st.image(img, caption="Lunar Map Preview", use_container_width=True)
        st.success("Map loaded successfully!")

except Exception as e:
    st.error(f"Error: {e}")