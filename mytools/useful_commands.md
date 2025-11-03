Data Path
```/mnt/ceph/users/neuro/wasp_em/83_milling_depth_variation_correction```

Visualize image volume
```chunkflow load-tif -f image.h5 neuroglancer```

Train cyclegan
```python train.py --dataroot ./datasets/bad_sample1 --name /mnt/home/yli10/ceph/milling/checkpoints/bad_sample1_cyclegan_100_100 --model cycle_gan --display_id -1 --input_nc 1 --output_nc 1 --preprocess crop```

Test cyclegan
```python test.py --dataroot ./datasets/13_wasp_sample3/vol_04000/img_zyx_4000-4256_3400-3656_8150-8406 --name /mnt/home/yli10/ceph/milling/checkpoints/sample3_cyclegan_100_100 --model cycle_gan --input_nc 1 --output_nc 1 --preprocess none --num_test 256```

Yuri's results path
```/mnt/ceph/users/neuro/wasp_em/ykreinin/For Yicong```