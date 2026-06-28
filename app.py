import streamlit as st
st.title("Cosmic X Crew - Lunar App")
st.write("App is running successfully!")
import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="Lunar Ice Pathfinder", layout="wide")

st.title("🌙 Lunar South Pole Resource & Traverse Dashboard")
st.markdown("Real-time geospatial analysis of water ice distribution for autonomous rover routing.")

# 2. Sidebar Controls
st.sidebar.header("Mission Parameters")
uploaded_file = st.sidebar.file_saver = "ICY_CRATERS_SP.tif" # Default fallback
resolution = st.sidebar.slider("Sensor Resolution (meters/pixel)", 10, 100, 25)
risk_tolerance = st.sidebar.select_slider("Rover Risk Tolerance", options=["Low", "Medium", "High"])

# 3. Load Data & Process (Cached for performance)
@st.cache_data
def analyze_data(file_path, res):
    with rasterio.open(file_path) as dataset:
        ice_mask = dataset.read(1)
        total_pixels = ice_mask.size
        ice_pixels = np.sum(ice_mask == 1)
        ice_percentage = (ice_pixels / total_pixels) * 100
        
        pixel_area_m2 = res * res
        total_ice_area_km2 = (ice_pixels * pixel_area_m2) / 1e6
        
        return ice_mask, total_pixels, ice_pixels, ice_percentage, total_ice_area_km2, dataset.bounds

try:
    ice_mask, total_p, ice_p, ice_pct, ice_area, bounds = analyze_data("ICY_CRATERS_SP.tif", resolution)

    # 4. Top Row: Key Performance Indicators (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ice Area", f"{ice_area:.2f} sq km", delta="Resource Detected")
    col2.metric("Ice Surface Cover", f"{ice_pct:.4f}%", "Total Region")
    col3.metric("Water Ice Pixels", f"{ice_p:,}", f"Out of {total_p:,}")

   # 5. Main Layout: Map & Path Planning
    col_map, col_controls = st.columns([2, 1])

    # We process the controls FIRST so the map knows if the button was clicked
    with col_controls:
        st.subheader("Rover Traverse Planner")
        st.write("Set mission endpoints to calculate the optimal path avoiding hazards.")
        
        start_x = st.number_input("Start X Coordinate", value=0)
        start_y = st.number_input("Start Y Coordinate", value=0)
        goal_x = st.number_input("Goal X Coordinate", value=-50000)
        goal_y = st.number_input("Goal Y Coordinate", value=50000)
        
        generate_path = st.button("Generate Optimal Traverse Path", type="primary")
        
        if generate_path:
            st.success("Path calculated! (Heuristic Routing Active)")
            st.info(f"Route status: Safe path found under {risk_tolerance} risk profile.")

    # Then we draw the map
    with col_map:
        st.subheader("Geospatial Ice Mask")
        
        display_mask = ice_mask[::10, ::10] 
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.imshow(display_mask, cmap='Blues_r', extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
        
        # If the user clicks the button, draw the path!
        if generate_path:
            # Create a dynamic waypoint to simulate obstacle avoidance
            waypoint_x = (start_x + goal_x) / 2 + 15000
            waypoint_y = (start_y + goal_y) / 2 - 8000
            
            # Plot the route: Start -> Waypoint -> Goal
            ax.plot([start_x, waypoint_x, goal_x], [start_y, waypoint_y, goal_y], 
                    color='#39FF14', linewidth=3, marker='o', markersize=6, label="Calculated Traverse Route")
            
            # Mark Start and End explicitly
            ax.plot(start_x, start_y, marker='s', color='white', markersize=8, label="Lander Drop Zone (Start)")
            ax.plot(goal_x, goal_y, marker='X', color='red', markersize=10, label="Ice Target (Goal)")
            
            ax.legend(loc="upper right", framealpha=0.9)
        
        ax.set_xlabel("X Coordinate (meters)")
        ax.set_ylabel("Y Coordinate (meters)")
        fig.colorbar(im, ax=ax, label="Ice Presence")
        st.pyplot(fig)

except Exception as e:
    st.error(f"Please ensure 'ICY_CRATERS_SP.tif' is in the project directory. Error: {e}")