from PIL import Image

# Open an image file
image = Image.open("/mnt/home/yli10/ceph/milling/13_wasp_sample3/vol_04000/img_zyx_3900-4356_3300-3756_8050-8506_translated_from_yz/yz/yz_0000.png")

# Define the crop rectangle (left, upper, right, lower)
crop_rectangle = (204, 174, 312, 282) #yz
# crop_rectangle = (174, 174, 282, 282) #xz

# Crop the image
cropped_image = image.crop(crop_rectangle)

# Save the cropped image
cropped_image.save("yz_0000_ours.png")
