import streamlit as st
import rasterio
import requests
import os

FILE_ID = "1R9OrT4NZDvzleV4Tc8OdPdV4lh0npv-N"
FILENAME = "ICY_CRATERS_SP.tif"

# 1. Download with proper headers
if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) < 1000000:
    st.write("Downloading data from Google Drive...")
    url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
    
    # We use a session to handle potential redirects
    session = requests.Session()
    response = session.get(url, stream=True)
    
    # Check if we got a real file and not an HTML page
    if response.status_code == 200:
        with open(FILENAME, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        st.write("Download complete!")
    else:
        st.error(f"Failed to download. Status code: {response.status_code}")

# 2. Add a check before opening
if os.path.exists(FILENAME):
    try:
        with rasterio.open(FILENAME) as src:
            st.write("File loaded successfully!")
            st.write(f"Metadata: {src.profile}") # This will print info if successful
    except Exception as e:
        st.error(f"Rasterio Error: {e}")
        st.write("The file might be corrupted or not a valid GeoTIFF.")
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