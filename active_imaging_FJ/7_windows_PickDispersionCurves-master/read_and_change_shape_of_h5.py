import h5py
import numpy as np

# 打开你的 .h5 文件
file_path = 'H:\\lhyonedrive\\OneDrive\\termite\\temple\\test\\arraylength_20.0m_offset_minoff_10.0m_spacing_0.5m_59-3_2024-05-14-07-00-30.110_output_right_sac_FJ_dispersion.h5'
with h5py.File(file_path, 'r+') as h5file:
    # 读取数据集
    ds = h5file['ds'][:]
    f = h5file['f'][:]
    c = h5file['c'][:]
    
    # 打印原始数据形状
    print(f"Original ds shape: {ds.shape}")
    
    # 获取频率和相速度的长度
    nf, nc = len(f), len(c)
    print(f"nf (length of f): {nf}")
    print(f"nc (length of c): {nc}")
    
    # 检查并调整 ds 数据的形状
    if ds.shape[2:] == (nf, nc):
        ds_new = ds.squeeze().transpose(1, 0, 2)  # 变换形状以匹配 (31, 100)
        print(f"Transformed ds shape: {ds_new.shape}")
        
        # 删除原始数据集并写入新数据集
        del h5file['ds']
        h5file.create_dataset('ds', data=ds_new)
    else:
        print("ds shape is already correct or requires different handling.")
