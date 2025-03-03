import pygrib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Open grib2 file
grbs = pygrib.open('usa_data.grib2')
grb = grbs[1]

# Get data and lat/lon
data, lats, lons = grb.data()

# Figure settings - remove margins
plt.figure(figsize=(8, 8))
ax = plt.gca()
ax.set_axis_off()

# Remove margins
plt.margins(0,0)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

# Visualize data - change to grayscale colormap
plt.pcolormesh(lons, lats, data, 
               cmap='Greys_r',     # Use Greys_r for inverted grayscale display
               norm=LogNorm(vmin=0.1, vmax=data.max()),
               )

# Remove unnecessary margins
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

# Save as PNG - set facecolor to black
plt.savefig('usa_data.png', 
            bbox_inches='tight', 
            pad_inches=0, 
            dpi=300,
            facecolor='black',  # Set background color to black
            edgecolor='none')
plt.close()