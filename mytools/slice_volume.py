#!/usr/bin/env python
"""Slice a 3D volume into PNG section images along the xy, xz and yz planes.

The volume is read in (z, y, x) order, z being the section (milling) axis.
Images are written as <out>/xy/xy_0000.png, <out>/xz/xz_0000.png and
<out>/yz/yz_0000.png with

    xy_i = volume[i, :, :]   (rows y, cols x)
    xz_i = volume[:, i, :]   (rows z, cols x)
    yz_i = volume[:, :, i]   (rows z, cols y)

Usage
    python slice_volume.py volume.h5                       # dataset 'main', all planes
    python slice_volume.py volume.h5 --key t0 --rgb        # other dataset, RGB PNGs
    python slice_volume.py volume.npy --planes xy yz --out slices
    python slice_volume.py volume.npy --axes zxy           # array stored as (z, x, y)

Output folder defaults to the input path without its extension. The whole
volume is loaded into memory.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

PLANES = ('xy', 'xz', 'yz')


def load_volume(path, key='main', axes='zyx'):
    """Return the volume as a (z, y, x) array."""
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.h5', '.hdf5', '.hdf'):
        import h5py
        with h5py.File(path, 'r') as f:
            if key not in f:
                sys.exit(f'{path} has no dataset {key!r}; top-level keys: {list(f.keys())}')
            obj = f[key]
            while isinstance(obj, h5py.Group):      # e.g. --key t0: take the first dataset below it
                if len(obj) == 0:
                    sys.exit(f'{path}:{obj.name} is an empty group')
                obj = obj[next(iter(obj))]
            print(f'reading {path}:{obj.name} shape {obj.shape} dtype {obj.dtype}')
            vol = obj[...]
    elif ext == '.npy':
        vol = np.load(path)
        print(f'reading {path} shape {vol.shape} dtype {vol.dtype}')
    else:
        sys.exit(f'unsupported input {path}: use .h5/.hdf5 or .npy')
    if vol.ndim != 3:
        sys.exit(f'expected a 3D volume, got shape {vol.shape}')
    if sorted(axes) != ['x', 'y', 'z']:
        sys.exit('--axes must be a permutation of xyz, e.g. zyx or zxy')
    if axes != 'zyx':
        vol = vol.transpose([axes.index(a) for a in 'zyx'])
    return vol


def to_uint8(vol):
    if vol.dtype == np.uint8:
        return vol
    lo, hi = float(vol.min()), float(vol.max())
    print(f'warning: {vol.dtype} volume rescaled from [{lo:g}, {hi:g}] to uint8')
    scale = 255.0 / (hi - lo) if hi > lo else 0.0
    return ((vol.astype(np.float64) - lo) * scale).round().astype(np.uint8)


def save_plane(vol, plane, out_dir, rgb=False, overwrite=False, every=50):
    n = vol.shape[PLANES.index(plane)]
    width = max(4, len(str(n - 1)))
    d = os.path.join(out_dir, plane)
    os.makedirs(d, exist_ok=True)
    if not overwrite and any(f.endswith('.png') for f in os.listdir(d)):
        sys.exit(f'{d} already contains PNG files; use --overwrite to replace them')
    for i in range(n):
        if i % every == 0:
            print(f'{plane}: {i}/{n}')
        if plane == 'xy':
            img = vol[i, :, :]
        elif plane == 'xz':
            img = vol[:, i, :]
        else:
            img = vol[:, :, i]
        im = Image.fromarray(np.ascontiguousarray(img))
        if rgb:
            im = im.convert('RGB')
        im.save(os.path.join(d, f'{plane}_{i:0{width}d}.png'))
    print(f'{plane}: wrote {n} images to {d}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('volume', help='input volume (.h5/.hdf5 or .npy)')
    p.add_argument('--key', default='main', help='HDF5 dataset (or group) holding the volume (default: main)')
    p.add_argument('--axes', default='zyx', help='axis order of the stored array (default: zyx)')
    p.add_argument('--planes', nargs='+', choices=PLANES, default=list(PLANES), help='planes to export (default: all)')
    p.add_argument('--out', help='output folder (default: input path without extension)')
    p.add_argument('--rgb', action='store_true', help='write 3-channel PNGs instead of 8-bit grey')
    p.add_argument('--overwrite', action='store_true', help='replace PNGs already present in the output folders')
    a = p.parse_args()

    if not os.path.isfile(a.volume):
        sys.exit(f'{a.volume}: no such file')
    vol = to_uint8(load_volume(a.volume, a.key, a.axes))
    out = a.out or os.path.splitext(a.volume)[0]
    print(f'volume (z, y, x) = {vol.shape}; writing to {out}')
    for plane in a.planes:
        save_plane(vol, plane, out, rgb=a.rgb, overwrite=a.overwrite)


if __name__ == '__main__':
    main()
