# 定义目录路径
$directoryPath = "E:\lhyonedrive\OneDrive\sym\truck\process\surface\line1_p\shots_240508_processed_sgy_1267_h5"

# 获取目录下所有的 .h5 文件
$h5Files = Get-ChildItem -Path $directoryPath -Filter *.h5

# 遍历所有文件
foreach ($file in $h5Files) {
    # 构建完整的文件路径
    $fullPath = $file.FullName
    
    # 调用 Python 脚本并传递文件路径
    python "E:\lhyonedrive\OneDrive\sym\truck\process\surface\PickDispersionCurves-master\PickDispersionCurves.py" $fullPath
}
