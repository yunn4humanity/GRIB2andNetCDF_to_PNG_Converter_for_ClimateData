import pygrib
import numpy as np
from datetime import datetime

def safe_get(grb, attr, default="Not available"):
    """Helper function to safely retrieve attributes"""
    try:
        return grb[attr] if attr in grb.keys() else default
    except:
        return default

def analyze_grib2(file_path):
    try:
        # Open GRIB2 file
        grbs = pygrib.open(file_path)
        
        print("=== GRIB2 File Structure Analysis ===\n")
        
        # Iterate through all messages
        for i, grb in enumerate(grbs, 1):
            print(f"\nMessage #{i}")
            print("="* 50)
            
            # 1. Indicator Section & 2. Identification Section
            print("\n[Identification Information]")
            print(f"• Issuing center: {safe_get(grb, 'centre')}")
            try:
                print(f"• Creation time: {datetime.fromtimestamp(grb.timeStamp)}")
            except:
                print("• Creation time: Not available")
            try:
                print(f"• Reference time: {grb.validDate}")
            except:
                print("• Reference time: Not available")
            
            # 4. Grid Description Section
            print("\n[Grid Information]")
            print(f"• Grid type: {safe_get(grb, 'gridType')}")
            print(f"• Number of grid points: {safe_get(grb, 'numberOfPoints')}")
            
            # Safely get latitude/longitude information
            try:
                lat_first = safe_get(grb, 'latitudeOfFirstGridPointInDegrees')
                lat_last = safe_get(grb, 'latitudeOfLastGridPointInDegrees')
                if lat_first != "Not available" and lat_last != "Not available":
                    print(f"• Latitude range: {lat_first:.2f}° ~ {lat_last:.2f}°")
                else:
                    print("• Latitude range: Not available")
            except:
                print("• Latitude range: Not available")
                
            try:
                lon_first = safe_get(grb, 'longitudeOfFirstGridPointInDegrees')
                lon_last = safe_get(grb, 'longitudeOfLastGridPointInDegrees')
                if lon_first != "Not available" and lon_last != "Not available":
                    print(f"• Longitude range: {lon_first:.2f}° ~ {lon_last:.2f}°")
                else:
                    print("• Longitude range: Not available")
            except:
                print("• Longitude range: Not available")
            
            # 5. Product Definition Section
            print("\n[Variable Information]")
            print(f"• Variable name: {safe_get(grb, 'name')}")
            print(f"• Units: {safe_get(grb, 'units')}")
            print(f"• Level: {safe_get(grb, 'level')}")
            
            # 6. Data Representation Section
            print("\n[Data Representation Information]")
            print(f"• Packing method: {safe_get(grb, 'packingType')}")
            print(f"• Missing value: {safe_get(grb, 'missingValue')}")
            
            # 7 & 8. Bitmap & Data Section
            try:
                data = grb.values
                print("\n[Data Statistics]")
                print(f"• Data shape: {data.shape}")
                print(f"• Minimum value: {np.min(data):.2f}")
                print(f"• Maximum value: {np.max(data):.2f}")
                print(f"• Mean value: {np.mean(data):.2f}")
                print(f"• Standard deviation: {np.std(data):.2f}")
            except:
                print("\n[Data Statistics]")
                print("• Unable to calculate data statistics.")
            
            # Print all available keys
            print("\n[All Available Keys]")
            for key in grb.keys():
                if key not in ['values', 'latitudes', 'longitudes'] and not key.startswith('_'):
                    print(f"• {key}: {safe_get(grb, key)}")
            
            print("\n" + "="*50)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
    finally:
        if 'grbs' in locals():
            grbs.close()

# Usage example
file_path = 'usa_data.grib2'  # Path to the GRIB2 file to analyze
analyze_grib2(file_path)