import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# Open NC file
ds = nc.Dataset('korea_data.nc', 'r')

# Check actual structure of DBZH variable
dbzh_var = ds.variables['DBZH']
print("DBZH variable dimensions:", dbzh_var.dimensions)
print("DBZH variable attributes:", dbzh_var.ncattrs())

# Read data
dbzh = dbzh_var[:]

# Handle missing values
if hasattr(dbzh_var, '_FillValue'):
    fill_value = dbzh_var._FillValue
    dbzh = np.ma.masked_equal(dbzh, fill_value)

# Attempt to reshape data
# Reshape according to actual data structure
try:
    # Example: assume time × altitude × distance
    reshaped_data = dbzh.reshape(-1, len(ds.variables['range'][:]))
    
    plt.figure(figsize=(12, 8))
    plt.pcolormesh(reshaped_data)
    plt.colorbar(label='DBZH (dBZ)')
    plt.title('Radar Reflectivity (DBZH) Distribution')
    plt.show()
    
except ValueError as e:
    print("Data reshape error:", e)

# Print detailed variable information
print("\nVariable information:")
for var_name in ds.variables:
    var = ds.variables[var_name]
    print(f"{var_name}:")
    print(f"  Dimensions: {var.dimensions}")
    print(f"  Shape: {var.shape}")
    print(f"  Attributes: {var.ncattrs()}")

ds.close()