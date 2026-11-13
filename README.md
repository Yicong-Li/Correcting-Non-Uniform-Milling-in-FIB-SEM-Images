# Correcting Non-Uniform Milling in FIB-SEM Images

Code for the paper [Correcting Non-Uniform Milling in FIB-SEM Images with Unsupervised Cross-Plane Image-to-Image Translation](https://www.biorxiv.org/content/10.1101/2025.09.29.679411v1).

A CycleGAN is trained to translate Y-Z (or X-Z) sections of a FIB-SEM volume into the style of its X-Y sections. Applying the trained generator to every Y-Z (or X-Z) section and restacking the results gives the corrected volume.

## Layout

- `methods/`: core model related scripts.
- `mytools/`: scripts to slice a volume into section images, to rebuild a volume from the translated images.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Volumes are HDF5 (dataset `main`) or `.npy` arrays in `(z, y, x)` order, with `z` the milling direction.

1. Slice the training volume and the volume to correct into section images:

   ```bash
   python mytools/slice_volume.py train_volume.h5 --planes xy yz
   python mytools/slice_volume.py test_volume.h5 --planes xy yz
   ```

   This writes `train_volume/xy`, `train_volume/yz`, and the same for `test_volume`.

2. Arrange them as a CycleGAN dataset (domain A: Y-Z sections, domain B: X-Y sections):

   ```bash
   mkdir -p methods/datasets/mydata
   ln -s /path/to/train_volume/yz methods/datasets/mydata/trainA
   ln -s /path/to/train_volume/xy methods/datasets/mydata/trainB
   ln -s /path/to/test_volume/yz  methods/datasets/mydata/testA
   ln -s /path/to/test_volume/xy  methods/datasets/mydata/testB
   ```

3. Train:

   ```bash
   cd methods
   python train.py --dataroot ./datasets/mydata --name myexp --model cycle_gan \
       --input_nc 1 --output_nc 1 --preprocess crop --display_id -1
   ```

4. Translate the test sections:

   ```bash
   python test.py --dataroot ./datasets/mydata --name myexp --model cycle_gan \
       --input_nc 1 --output_nc 1 --preprocess none --num_test <number of yz sections>
   ```

   With `--preprocess none` the section width and height must be multiples of 4. The translated sections are written to `methods/results/myexp/test_latest/images/*_fake_B.png`.

5. Rebuild the corrected volume:

   ```bash
   cd ..
   python mytools/reconstruct_volume.py methods/results/myexp/test_latest/images corrected.h5 --like test_volume.h5
   ```

To correct along the other axis, use `xz` instead of `yz` in steps 1, 2 and 5 (`--plane xz`).

## Citation

```bibtex
@article{li2025milling,
  title   = {Correcting Non-Uniform Milling in FIB-SEM Images with Unsupervised Cross-Plane Image-to-Image Translation},
  author  = {Li, Yicong and Kreinin, Yuri and Zhang, Lewei and Huang, Siyu and Schomburg, Erik W. and Chklovskii, Dmitri B. and Pfister, Hanspeter and Wu, Jingpeng},
  journal = {bioRxiv},
  year    = {2025},
  doi     = {10.1101/2025.09.29.679411}
}
```

## License

BSD 3-Clause.
