import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def analyze_netcdf_radar(file_path):
   # Read NetCDF file
   ds = xr.open_dataset(file_path)
   
   # 1. Time information analysis
   print("\n=== 1. Time Information Analysis ===")
   print(f"Start time: {ds.time_coverage_start.values}")
   print(f"End time: {ds.time_coverage_end.values}")
   print("\nTime range:")
   print(f"First time: {ds.time.values[0]}")
   print(f"Last time: {ds.time.values[-1]}")
   
   # 2. Major radar variable analysis
   radar_vars = ['DBZH', 'DBZV', 'UH', 'UV', 'VELH', 'VELV', 'ZDR', 'KDP', 'RHOHV']
   
   print("\n=== 2. Major Radar Variable Analysis ===")
   for var_name in radar_vars:
       if var_name in ds:
           data = ds[var_name].values
           print(f"\n{var_name} Statistics:")
           print(f"Shape: {data.shape}")
           print(f"Number of missing values: {np.sum(np.isnan(data))}")
           print(f"Missing value ratio: {(np.sum(np.isnan(data)) / data.size) * 100:.2f}%")
           valid_data = data[~np.isnan(data)]
           if len(valid_data) > 0:
               print(f"Valid data range: {np.min(valid_data):.2f} ~ {np.max(valid_data):.2f}")
               print(f"Mean value: {np.mean(valid_data):.2f}")
               print(f"Median value: {np.median(valid_data):.2f}")
   
   # 3. Multi-variable analysis by sweep
   print("\n=== 3. Multi-variable Analysis by Sweep ===")
   
   # Output sweep information
   print("\nSweep information:")
   print(f"Elevation angles: {ds.fixed_angle.values}")
   print(f"Sweep mode: {ds.sweep_mode.values}")
   
   for sweep_idx in range(len(ds.sweep_start_ray_index)):
       print(f"\nSweep {sweep_idx} Analysis:")
       print(f"Elevation angle: {ds.fixed_angle.values[sweep_idx]} degrees")
       
       start_idx = ds.sweep_start_ray_index[sweep_idx].values
       end_idx = ds.sweep_end_ray_index[sweep_idx].values
       
       # Analysis for each variable
       for var_name in radar_vars:
           if var_name in ds:
               start_gate_idx = start_idx * len(ds['range'])
               end_gate_idx = (end_idx + 1) * len(ds['range'])
               sweep_data = ds[var_name].values[start_gate_idx:end_gate_idx].reshape(-1, len(ds['range']))
               
               valid_data = sweep_data[~np.isnan(sweep_data)]
               if len(valid_data) > 0:
                   print(f"\n{var_name}:")
                   print(f"Number of valid data points: {len(valid_data)}")
                   print(f"Data range: {np.min(valid_data):.2f} ~ {np.max(valid_data):.2f}")
                   
                   # Data distribution visualization
                   plt.figure(figsize=(12, 5))
                   
                   # subplot 1: histogram
                   plt.subplot(121)
                   plt.hist(valid_data, bins=50, density=True)
                   plt.title(f'{var_name} Distribution - Sweep {sweep_idx}')
                   plt.xlabel('Value')
                   plt.ylabel('Density')
                   
                   # subplot 2: 2D plot
                   plt.subplot(122)
                   plt.imshow(sweep_data, cmap='rainbow', origin='lower')
                   plt.colorbar(label=f'{var_name} [{ds[var_name].units}]')
                   plt.title(f'{var_name} Data - Sweep {sweep_idx}')
                   
                   plt.tight_layout()
                   plt.savefig(f'{var_name}_sweep_{sweep_idx}_analysis.png')
                   plt.close()

   ds.close()

# Execute function
analyze_netcdf_radar('korea_data.nc')