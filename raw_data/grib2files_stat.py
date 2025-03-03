import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import tqdm.auto as tqdm  # This part has been modified

def analyze_missing_values():
    # Find all .grib2 files in the current directory (place this file in the same directory as the grib2 files)
    grib_files = [f for f in os.listdir() if f.endswith('.grib2')]
    
    if not grib_files:
        print("No .grib2 files found in the current folder.")
        return
    
    print(f"Analyzing {len(grib_files)} .grib2 files.")
    
    # Dictionary to store missing value ratios
    missing_ratios = {}
    
    # Analyze each file
    progress_bar = tqdm.tqdm(grib_files, desc="Analyzing files")  
    for grib_file in progress_bar:
        try:
            # Read grib file
            ds = xr.open_dataset(grib_file, engine='cfgrib')
            
            # Select first variable (usually precipitation rate)
            var_name = list(ds.data_vars)[0]
            data = ds[var_name].values
            
            # Calculate missing value ratio (percentage of nan values)
            missing_ratio = (np.isnan(data).sum() / data.size) * 100
            missing_ratios[grib_file] = missing_ratio
            
            # Close dataset
            ds.close()
            
        except Exception as e:
            print(f'\nError analyzing file {grib_file}: {str(e)}')
            continue
    
    # Output results and visualization
    print("\nMissing value analysis results:")
    print("\nTop 10 files with highest missing values:")
    sorted_files = sorted(missing_ratios.items(), key=lambda x: x[1], reverse=True)
    for file, ratio in sorted_files[:10]:
        print(f"{file}: {ratio:.2f}%")
    
    # Draw histogram
    plt.figure(figsize=(10, 6))
    plt.hist(list(missing_ratios.values()), bins=50)
    plt.title('Missing Value Distribution in GRIB2 Files')
    plt.xlabel('Missing Value Ratio (%)')
    plt.ylabel('Number of Files')
    plt.grid(True)
    plt.savefig('missing_values_distribution.png')
    plt.close()
    
    # Output basic statistics
    ratios = np.array(list(missing_ratios.values()))
    print(f"\nBasic Statistics:")
    print(f"Mean missing value ratio: {np.mean(ratios):.2f}%")
    print(f"Median: {np.median(ratios):.2f}%")
    print(f"Minimum: {np.min(ratios):.2f}%")
    print(f"Maximum: {np.max(ratios):.2f}%")
    
    return missing_ratios

if __name__ == "__main__":
    # Instructions for installing required packages
    try:
        import xarray as xr
        import cfgrib
    except ImportError:
        print("Please install the required packages:")
        print("pip install xarray cfgrib tqdm matplotlib numpy")
        exit(1)
    
    missing_ratios = analyze_missing_values()