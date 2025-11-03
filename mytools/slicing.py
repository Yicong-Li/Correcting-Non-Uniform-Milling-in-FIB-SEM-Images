import h5py
from PIL import Image
import os

volume_path = "/mnt/home/yli10/ceph/milling/13_wasp_sample3/vol_04000/img_zyx_3900-4356_3300-3756_8050-8506.h5"
f_volume = h5py.File(volume_path, 'r')
print(f_volume.keys())
volume = f_volume['main'][:]
print(volume.shape)
f_volume.close()

# The volume follows zyx.
for i in range(volume.shape[0]):
    if i % 50 == 0:
        print(f"Processing {i}-th image......")
    # xy
    img_xy = volume[i, :, :]
    # xz
    img_xz = volume[:, i, :]
    # yz
    img_yz = volume[:, :, i]

    img_xy = Image.fromarray(img_xy)
    img_xz = Image.fromarray(img_xz)
    img_yz = Image.fromarray(img_yz)

    img_xy.save(os.path.join(volume_path[:-3], 'xy', 'xy_'+str(i).zfill(4)+'.png'))
    img_xz.save(os.path.join(volume_path[:-3], 'xz', 'xz_'+str(i).zfill(4)+'.png'))
    img_yz.save(os.path.join(volume_path[:-3], 'yz', 'yz_'+str(i).zfill(4)+'.png'))