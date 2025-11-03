import os
from PIL import Image
import numpy as np

folder_path = '/mnt/home/yli10/ceph/milling/checkpoints/sample3_cyclegan_100_100/test_latest/images'
images_list = os.listdir(folder_path)
images_pred = []

for i in images_list:
    if 'fake_B' in i:
        images_pred.append(i)

images_pred.sort()

images = []
for i in images_pred:
    print(i)
    img = np.array(Image.open(os.path.join(folder_path, i)))
    images.append(img[:, :, 0])

np.save('/mnt/home/yli10/ceph/milling/13_wasp_sample3/vol_04000/img_zyx_3900-4356_3300-3756_8050-8506_translated_from_yz.npy', np.array(images).transpose(1,0,2))
