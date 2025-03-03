import pygrib
import numpy as np
import matplotlib.pyplot as plt

# Open grib2 file
grbs = pygrib.open('usa_data.grib2')
grb = grbs[1]
data, lats, lons = grb.data()

data_flat = data.flatten()
lower_bound = -1000
upper_bound = 1000

# Select data within range
masked_data = data_flat[(data_flat >= lower_bound) & (data_flat <= upper_bound)]

# Check unique values
unique_values = np.unique(masked_data)
print("Number of unique values:", len(unique_values))
print("List of unique values (first 20):")
print(unique_values[:20])

# Draw histogram (increase number of bins and apply log scale)
plt.figure(figsize=(12, 6))

# Subplot 1: Normal scale
plt.subplot(1, 2, 1)
plt.hist(masked_data, bins=1000)
plt.title("Normal Scale")
plt.xlabel("Value")
plt.ylabel("Frequency")

# Subplot 2: Log scale
plt.subplot(1, 2, 2)
plt.hist(masked_data, bins=1000)
plt.yscale('log')  # Set y-axis to log scale
plt.title("Log Scale")
plt.xlabel("Value")
plt.ylabel("Frequency (log)")

plt.tight_layout()
plt.show()

# Print detailed statistics
print("\nDetailed Statistics:")
print(f"Data range: {np.min(masked_data):.10f} ~ {np.max(masked_data):.10f}")
print(f"Mean value: {np.mean(masked_data):.10f}")
print(f"Median value: {np.median(masked_data):.10f}")
print(f"Standard deviation: {np.std(masked_data):.10f}")