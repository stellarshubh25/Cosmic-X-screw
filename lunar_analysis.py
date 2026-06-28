import streamlit as st
import rasterio
import rasterio.enums

# Your Dropbox direct link
DIRECT_URL = "https://www.dropbox.com/scl/fi/ilu80zbhluyluq6pcd516/ICY_CRATERS_SP.tif?rlkey=g2jqntrpris2lydo3i8qdx22g&st=g5mumz31&dl=1"

st.title("Cosmic X Crew - Lunar Analysis")

# This is the ONLY try block you need
try:
    with rasterio.open(DIRECT_URL) as src:
        st.write("Successfully connected to the map data!")
        
        # This displays the image efficiently
        map_data = src.read(1, out_shape=(1, 1000, 1000), resampling=rasterio.enums.Resampling.bilinear)
        
        st.image(map_data, caption="Lunar Map Preview", use_container_width=True)
        st.success("Map loaded successfully!")

except Exception as e:
    st.error(f"Error: {e}")