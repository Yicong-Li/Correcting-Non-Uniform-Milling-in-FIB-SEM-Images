from PIL import Image
import os
import numpy as np

volume_path = "/mnt/home/yli10/ceph/milling/13_wasp_sample3/vol_04000/img_zyx_3900-4356_3300-3756_8050-8506_translated_from_yz.npy"
volume = np.load(volume_path).transpose(0, 2, 1)
print(volume.shape)

for i in range(volume.shape[0]):
    if i % 50 == 0:
        print(f"Processing {i}-th image......")
    # xy
    img_xy = volume[i, :, :]
    # xz
    img_xz = volume[:, i, :]
    # yz
    img_yz = volume[:, :, i]

    img_xy = Image.fromarray(img_xy).convert('RGB')
    img_xz = Image.fromarray(img_xz).convert('RGB')
    img_yz = Image.fromarray(img_yz).convert('RGB')

    img_xy.save(os.path.join(volume_path[:-4], 'xy', 'xy_'+str(i).zfill(4)+'.png'))
    img_xz.save(os.path.join(volume_path[:-4], 'xz', 'xz_'+str(i).zfill(4)+'.png'))
    img_yz.save(os.path.join(volume_path[:-4], 'yz', 'yz_'+str(i).zfill(4)+'.png'))