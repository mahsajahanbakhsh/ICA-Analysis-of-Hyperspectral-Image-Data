# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:56:04 2026

@author: Mahsa
"""

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA, PCA
from scipy.io import loadmat
from scipy.stats import skew, kurtosis

from google.colab import files
# Load the MAT file
mat_data = loadmat('Indian_pines_corrected.mat')
img_data = mat_data['indian_pines_corrected']  # Access the corrected hyperspectral data

# Check the shape of the data
print(f"Data shape: {img_data.shape}")  # Expected output: (145, 145, 200)
# Reshape the data for ICA processing
n_samples = img_data.shape[0] * img_data.shape[1]  # Total number of pixels
n_bands = img_data.shape[2]  # Number of spectral bands
img_data_reshaped = img_data.reshape(n_samples, n_bands)  # Reshape to (N, bands)

# Apply PCA to whiten the data
pca = PCA(whiten=True, random_state=0)
img_data_whitened = pca.fit_transform(img_data_reshaped)

# Apply ICA
n_components = min(n_bands, img_data_reshaped.shape[0])  # Set appropriate component size
ica = FastICA(n_components=n_components, max_iter=1000, tol=0.001, random_state=0)
ica_transformed = ica.fit_transform(img_data_whitened)
# Analyze independent components
skewness_values = skew(ica_transformed, axis=0)
kurtosis_values = kurtosis(ica_transformed, axis=0, fisher=True)

# Rank components by a combined measure of skewness and kurtosis
rank_criterion = np.abs(skewness_values) + np.abs(kurtosis_values)
ranked_indices = np.argsort(rank_criterion)[::-1]

# Generate a report for the ranked components
def generate_component_report(ranked_indices, skewness_values, kurtosis_values, ica_transformed):
    print("Component Ranking Report")
    print("========================")
    for rank, idx in enumerate(ranked_indices[:20], start=1):
        mean_val = np.mean(ica_transformed[:, idx])
        var_val = np.var(ica_transformed[:, idx])
        print(f"Rank {rank}: Component {idx + 1}")
        print(f"  Mean: {mean_val:.3f}, Variance: {var_val:.3f}")
        print(f"  Skewness: {skewness_values[idx]:.3f}, Kurtosis: {kurtosis_values[idx]:.3f}")
        print(f"  Combined Rank Metric: {rank_criterion[idx]:.3f}")
        print("-" * 40)

generate_component_report(ranked_indices, skewness_values, kurtosis_values, ica_transformed)

# Construct an RGB image using the first three ranked ICs
def create_rgb_image(ica_transformed, ranked_indices, image_shape):
    rgb_image = np.zeros((image_shape[0], image_shape[1], 3))
    
    for i in range(3):
        component_index = ranked_indices[i]
        component_image = ica_transformed[:, component_index].reshape(image_shape)
        component_image_normalized = (component_image - component_image.min()) / component_image.ptp()
        rgb_image[:,:,i] = component_image_normalized
    
    return rgb_image

# Creating and displaying the RGB image
rgb_image = create_rgb_image(ica_transformed, ranked_indices, (145, 145))
plt.imshow(rgb_image)
plt.title('RGB Image from Top 3 ICs')
plt.axis('off')
plt.show()
# Visualize the component ranking with improved x-axis labeling
def plot_component_ranking(rank_criterion, ranked_indices):
    plt.figure(figsize=(16, 8))  # Increase figure size for better spacing
    sorted_indices = range(1, len(rank_criterion) + 1)
    
    # Plot the bar chart
    plt.bar(sorted_indices, rank_criterion[ranked_indices], color='skyblue')
    
    # Set labels and title
    plt.title('Ranking of Components Based on Skewness and Kurtosis')
    plt.xlabel('Component Number')
    plt.ylabel('Rank (|Skewness| + |Kurtosis|)')
    
    # Select a subset of labels to avoid overlap
    displayed_labels = [f'IC {i+1}' for j, i in enumerate(ranked_indices) if j % 5 == 0]
    displayed_ticks = [j+1 for j in range(len(ranked_indices)) if j % 5 == 0]
    
    # Apply the selected subset of tick labels
    plt.xticks(ticks=displayed_ticks, labels=displayed_labels, rotation=45, ha='right', fontsize=9)
    
    # Add grid for better readability
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot the ranking
plot_component_ranking(rank_criterion, ranked_indices)

# Visualize the top components
plt.figure(figsize=(15, 10))
for i, idx in enumerate(ranked_indices[:20], 1):
    component_image = ica_transformed[:, idx].reshape((145, 145))
    plt.subplot(4, 5, i)
    plt.imshow(component_image, cmap='gray')
    plt.title(f'IC {idx}')
    plt.axis('off')

plt.suptitle('Top 20 Independent Components Visualization')
plt.show()
# Visualize histograms of top components
plt.figure(figsize=(15, 10))
for i, idx in enumerate(ranked_indices[:20], 1):
    plt.subplot(4, 5, i)
    plt.hist(ica_transformed[:, idx], bins=30, color='gray', alpha=0.7)
    plt.title(f'IC {idx} Histogram')
    plt.grid(True)

plt.suptitle('Histograms of Top 20 Independent Components')
plt.tight_layout()
plt.show()
