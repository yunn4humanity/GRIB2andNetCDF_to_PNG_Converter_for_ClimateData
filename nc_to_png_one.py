import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

def radar_to_cartesian(file_path, variable='DBZH'):
   ds = xr.open_dataset(file_path)
   
   for sweep_idx in range(len(ds.sweep_start_ray_index)):
       start_idx = ds.sweep_start_ray_index[sweep_idx].values
       end_idx = ds.sweep_end_ray_index[sweep_idx].values
       
       start_gate_idx = start_idx * len(ds['range'])
       end_gate_idx = (end_idx + 1) * len(ds['range'])
       sweep_data = ds[variable].values[start_gate_idx:end_gate_idx].reshape(-1, len(ds['range']))
       
       if sweep_data.size > 0:
           # Azimuth and range information
           azimuths = np.radians(ds.azimuth[start_idx:end_idx+1].values)
           ranges = ds.range.values
           
           # Create meshgrid the same size as sweep_data
           r, az = np.meshgrid(ranges, azimuths[:sweep_data.shape[0]])
           
           # Convert polar coordinates to cartesian coordinates
           x = r * np.sin(az)
           y = r * np.cos(az)
           
           # Print sizes for verification
           print(f"x shape: {x.shape}")
           print(f"y shape: {y.shape}")
           print(f"sweep_data shape: {sweep_data.shape}")
           
           # Create plot
           fig = plt.figure(figsize=(10, 10), facecolor='black')
           ax = plt.axes(facecolor='black')
           
           # Plot data
           mesh = ax.pcolormesh(x/1000, y/1000, sweep_data,
                              cmap='Greys_r',
                              vmin=-20,
                              vmax=80)
           
           ax.set_aspect('equal')
           ax.set_xticks([])
           ax.set_yticks([])
           ax.set_xticklabels([])
           ax.set_yticklabels([])
           plt.axis('off')
           
           plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
           plt.margins(0,0)
           
           plt.savefig(f'radar_cartesian_sweep_{sweep_idx}.png', 
                      bbox_inches='tight', 
                      pad_inches=0,
                      dpi=300,
                      facecolor='black',
                      edgecolor='none')
           plt.close()
           
   ds.close()

# Execute function
radar_to_cartesian('korea_data.nc', 'DBZH')