#!/usr/bin/env python
"""Rebuild a 3D volume from the section images written by CycleGAN's test.py.

test.py writes <results_dir>/<name>/test_latest/images/<plane>_<index>_<tag>.png,
for example yz_0000_fake_B.png. This script stacks the images carrying one tag
back into a (z, y, x) volume:

    yz images (rows z, cols y): image i -> volume[:, :, i]
    xz images (rows z, cols x): image i -> volume[:, i, :]

Usage
    python reconstruct_volume.py results/exp/test_latest/images corrected.h5
    python reconstruct_volume.py results/exp/test_latest/images corrected.npy --plane xz
    python reconstruct_volume.py results/exp/test_latest/images corrected.h5 --like original.h5

--like copies the voxel_offset and voxel_size datasets of another HDF5 volume,
if present, so the result can be viewed next to it.

The input images are expected to be named as slice_volume.py names them,
<plane>_<index>.png, which test.py extends to <plane>_<index>_<tag>.png.
"""
import argparse
import os
import re
import sys

import numpy as np
from PIL import Image


def list_images(folder, plane, tag):
    if not os.path.isdir(folder):
        sys.exit(f'{folder}: no such folder')
    pat = re.compile(rf'^{plane}_(\d+)_{re.escape(tag)}\.png$')
    found = {}
    for name in os.listdir(folder):
        m = pat.match(name)
        if m:
            found[int(m.group(1))] = os.path.join(folder, name)
    if not found:
        sys.exit(f'no {plane}_*_{tag}.png files in {folder}')
    n = max(found) + 1
    missing = [i for i in range(n) if i not in found]
    if missing:
        sys.exit(f'{len(missing)} missing indices (first: {missing[:5]}); expected 0..{n - 1}')
    return [found[i] for i in range(n)]


def read_grey(path):
    arr = np.array(Image.open(path))
    return arr[..., 0] if arr.ndim == 3 else arr      # RGB outputs carry the same value in all channels


def reconstruct(files, plane, every=50):
    first = read_grey(files[0])
    n = len(files)
    if plane == 'yz':
        vol = np.empty((first.shape[0], first.shape[1], n), np.uint8)
    else:
        vol = np.empty((first.shape[0], n, first.shape[1]), np.uint8)
    for i, f in enumerate(files):
        if i % every == 0:
            print(f'{i}/{n}')
        img = read_grey(f)
        if img.shape != first.shape:
            sys.exit(f'{f} has shape {img.shape}, expected {first.shape}')
        if plane == 'yz':
            vol[:, :, i] = img
        else:
            vol[:, i, :] = img
    return vol


def save(vol, path, like=None, overwrite=False):
    if os.path.exists(path) and not overwrite:
        sys.exit(f'{path} exists; use --overwrite to replace it')
    ext = os.path.splitext(path)[1].lower()
    if ext == '.npy':
        np.save(path, vol)
    elif ext in ('.h5', '.hdf5', '.hdf'):
        import h5py
        with h5py.File(path, 'w') as f:
            f.create_dataset('main', data=vol, chunks=(1,) + vol.shape[1:], compression='gzip')
            if like:
                with h5py.File(like, 'r') as g:
                    for k in ('voxel_offset', 'voxel_size'):
                        if k in g:
                            f.create_dataset(k, data=g[k][...])
    else:
        sys.exit(f'unsupported output {path}: use .h5/.hdf5 or .npy')
    print(f'wrote {path} with shape (z, y, x) = {vol.shape}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('images', help='folder with the test.py output images')
    p.add_argument('output', help='output volume (.h5/.hdf5 or .npy)')
    p.add_argument('--plane', choices=('yz', 'xz'), default='yz', help='plane of the translated images (default: yz)')
    p.add_argument('--tag', default='fake_B', help='image tag to stack (default: fake_B, the translated images)')
    p.add_argument('--like', help='HDF5 volume whose voxel_offset/voxel_size datasets are copied')
    p.add_argument('--overwrite', action='store_true', help='replace an existing output file')
    a = p.parse_args()

    files = list_images(a.images, a.plane, a.tag)
    print(f'{len(files)} {a.plane} images tagged {a.tag}')
    save(reconstruct(files, a.plane), a.output, a.like, a.overwrite)


if __name__ == '__main__':
    main()
