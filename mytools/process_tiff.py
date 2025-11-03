import tifffile as tiff
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the TIFF file
original_path = '/mnt/ceph/users/neuro/wasp_em/ykreinin/For Yicong/orginal_map_x-224.tif'
stephen_path = '/mnt/ceph/users/neuro/wasp_em/ykreinin/For Yicong/stephen_map_x-224.tif'
transxz_path = '/mnt/ceph/users/neuro/wasp_em/ykreinin/For Yicong/trans_xz_map_x-224.tif'
transyz_path = '/mnt/ceph/users/neuro/wasp_em/ykreinin/For Yicong/trans_yz_map_x-224.tif'

original = tiff.imread(original_path) / 1000.0
stephen = tiff.imread(stephen_path) / 1000.0
transxz = tiff.imread(transxz_path) / 1000.0
transyz = tiff.imread(transyz_path) / 1000.0

# Combine all images into a list
images = [original, stephen, transxz, transyz]
titles = ['Original', 'Hanslovsky et al. [8]', 'X-Z Correction', 'Y-Z Correction']
colormap = 'inferno'

# Define a global min and max for the colormap based on all images
vmin = np.min([img.min() for img in images])
vmax = np.max([img.max() for img in images])

# Plot images with a shared colorbar
fig, axes = plt.subplots(1, 4, figsize=(10, 5))

for ax, img, title in zip(axes, images, titles):
    im = ax.imshow(img, cmap=colormap, vmin=vmin, vmax=vmax)
    ax.set_title(title, fontdict={'fontsize': 9, 'fontweight': 'bold', 'fontname': 'serif'}, pad=5)
    ax.axis('off')

# Adjust spacing between images
plt.subplots_adjust(wspace=0.05)  # Minimize horizontal space between images

# Add a single colorbar to the right of the row
cbar = fig.colorbar(im, ax=axes, orientation='vertical', fraction=0.015, pad=0.01)
# cbar.set_label('Intensity')

# Save the plot as an image file without boundaries
output_path = 'distance_colormap.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0)
# plt.show()