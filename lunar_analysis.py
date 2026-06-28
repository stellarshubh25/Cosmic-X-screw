import streamlit as st
import rasterio
import requests
import os

# Your specific file ID
FILE_ID = "1R9OrT4NZDvzleV4Tc8OdPdV4lh0npv-N"
FILENAME = "ICY_CRATERS_SP.tif"

# Download the file from Google Drive if it isn't already there
if not os.path.exists(FILENAME):
    st.write("Downloading data from Google Drive... (this may take a moment)")
    url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
    response = requests.get(url)
    with open(FILENAME, "wb") as f:
        f.write(response.content)
    st.write("Download complete!")

# Now proceed with your analysis using the file
with rasterio.open(FILENAME) as src:
    # Your existing code to process the image goes here
    st.write("File loaded and ready for analysis!")
# 1. Define the path to your GeoTIFF file
file_path = "ICY_CRATERS_SP.tif"

try:
    # 2. Open the GeoTIFF file
    with rasterio.open(file_path) as dataset:
        print("=" * 50)
        print("          LUNAR GEOTIFF METADATA          ")
        print("=" * 50)
        print(f"File Name:     {dataset.name}")
        print(f"Image Width:   {dataset.width} pixels")
        print(f"Image Height:  {dataset.height} pixels")
        print(f"Count of Bands:{dataset.count}")
        print(f"Coordinate Reference System (CRS):\n{dataset.crs}")
        print(f"Geotransform Matrix:\n{dataset.transform}")
        print("=" * 50)

        # 3. Read the first band (binary mask: 1 = ice, 0 = no ice)
        ice_mask = dataset.read(1)

        # 4. Perform Data Calculations
        # Total pixels in the image
        total_pixels = ice_mask.size
        
        # Count pixels containing water ice (where value == 1)
        ice_pixels = np.sum(ice_mask == 1)
        
        # Calculate percentages
        ice_percentage = (ice_pixels / total_pixels) * 100

        # Given: 25m resolution means each pixel is 25 meters x 25 meters
        pixel_resolution_m = 25 
        pixel_area_m2 = pixel_resolution_m * pixel_resolution_m
        
        # Convert total ice area to square kilometers (1 km² = 1,000,000 m²)
        total_ice_area_km2 = (ice_pixels * pixel_area_m2) / 1e6

        print("\n" + "=" * 50)
        print("          ICE DISTRIBUTION ANALYSIS       ")
        print("=" * 50)
        print(f"Total Pixels Scanned: {total_pixels:,}")
        print(f"Water Ice Pixels:     {ice_pixels:,}")
        print(f"Ice Surface Cover:    {ice_percentage:.4f}%")
        print(f"Total Estimated Ice Area: {total_ice_area_km2:.2f} sq km")
        print("=" * 50)

        # 5. Visualization
        print("\nGenerating visualization...")
        plt.figure(figsize=(10, 10))
        
        # Using a specialized colormap: 'Blues' makes ice (1) stand out against background (0)
        plt.imshow(ice_mask, cmap='Blues_r', extent=[
            dataset.bounds.left, dataset.bounds.right, 
            dataset.bounds.bottom, dataset.bounds.top
        ])
        
        plt.title("Lunar South Pole (85°–90°S) - Water Ice Binary Mask\nResolution: 25m/pixel", fontsize=14)
        plt.xlabel("X Coordinate (meters / Polar Stereographic)", fontsize=10)
        plt.ylabel("Y Coordinate (meters / Polar Stereographic)", fontsize=10)
        plt.colorbar(label="Ice Presence (Darker = Ice detected)")
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # Save the map locally and show it
        plt.savefig("lunar_ice_map.png", dpi=300, bbox_inches='tight')
        print("Map successfully saved as 'lunar_ice_map.png'")
        plt.show()

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please ensure it's in the same directory as this script.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")