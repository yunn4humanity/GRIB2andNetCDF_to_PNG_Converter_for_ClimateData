import pygrib

# Open GRIB file
grbs = pygrib.open('usa_data.grib2')

# Print all messages
for grb in grbs:
    print(grb)

# Select specific message and read data
grb = grbs.select()[0]  # First message
data = grb.values  # Data values
lats, lons = grb.latlons()  # Latitude/longitude grid

print(data)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.pcolormesh(lons, lats, data)
plt.colorbar(label='Reflectivity (dBZ)')
plt.title('MRMS Composite Reflectivity')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()