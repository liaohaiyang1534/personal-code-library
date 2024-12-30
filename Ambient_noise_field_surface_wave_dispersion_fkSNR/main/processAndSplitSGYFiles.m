function [cellArray] = processAndSplitSGYFiles(fileExtension, npts)
    % 调用文件选择历史管理工具
    [selectedRecord, historyFilePath] = manageFileSelectionHistory(fileExtension);

    % 提取用户选择记录的执行时间、路径和文件名
    timeStamp = selectedRecord.timeStamp;
    pathName = selectedRecord.pathName;
    fileNames = selectedRecord.fileNames;
    
    % 生成文件名
    formattedTimeStamp = regexprep(timeStamp, '[: -]', ''); % 删除时间戳中的特殊字符
    [~, folderName] = fileparts(pathName);
    firstFileName = fileNames{1}; % 只取第一个文件名
    cleanFileName = regexprep(firstFileName, '[^a-zA-Z0-9]', ''); % 移除非法字符
    generatedFileName = sprintf('cellArray_%s_%s_%s.mat', formattedTimeStamp, folderName, cleanFileName); % 拼接生成最终文件名
    
    % 获取存储路径
    [historyFolder, ~, ~] = fileparts(historyFilePath); % 提取 historyFilePath 的目录
    finalFilePath = fullfile(historyFolder, generatedFileName); % 拼接路径

    % 检查文件是否存在
    if isfile(finalFilePath)
        disp('==========================================');
        disp('文件已存在，直接读取 mat 文件 !');
        cellArray = load(finalFilePath).cellArray; % 读取文件内容
        disp(['切分后的 cell 数组大小: 1 x ', num2str(size(cellArray, 2))]);
        disp(['每个 cell 包含的矩阵大小: ', num2str(size(cellArray{1}, 1)), ' x ', num2str(size(cellArray{1}, 2))]);
        disp('==========================================');
        return;
    end

    % 初始化变量
    numFiles = length(fileNames);

    % --- 加载第一个文件以估算总块数 ---
    firstFilePath = fullfile(pathName, fileNames{1});
    try
        [FirstData, ~, ~] = ReadSegyFast(firstFilePath); % 加载第一个文件
    catch
        error(['读取文件失败: ', fileNames{1}, newline, ...
               '请检查文件路径或格式是否正确。']);
    end

    % 估算总块数
    totalRowsFirst = size(FirstData, 1);
    validRowsFirst = floor(totalRowsFirst / npts) * npts; % 计算有效行数
    numBlocksFirst = validRowsFirst / npts; % 第一个文件的块数
    expectedCols = size(FirstData, 2); % 使用第一个文件的列数
    estimatedTotalBlocks = numBlocksFirst * numFiles; % 假设每个文件的行数一致

    % 预分配 cellArray
    cellArray = cell(1, expectedCols);
    for col = 1:expectedCols
        cellArray{col} = zeros(npts, estimatedTotalBlocks); % 为每列分配固定大小的矩阵
    end

    % --- 开始加载并处理 SGY 文件 ---
    disp('--- 开始加载并处理 SGY 文件 ---');
    currentBlockIndex = 1;
    forProgress(numFiles);
    for i = 1:numFiles
        filePath = fullfile(pathName, fileNames{i});
        try
            [Data, ~, ~] = ReadSegyFast(filePath); % 加载 SGY 文件
        catch
            error(['读取文件失败: ', fileNames{i}, newline, ...
                   '请检查文件路径或格式是否正确。']);
        end

        % 检查文件列数是否一致
        if size(Data, 2) ~= expectedCols
            error(['文件列数不一致！文件: ', fileNames{i}, newline, ...
                   '该文件列数为: ', num2str(size(Data, 2)), ', 期望列数为: ', num2str(expectedCols), '.', newline, ...
                   '请检查文件格式是否正确。']);
        end

        % 按文件切分数据
        totalRows = size(Data, 1);
        validRows = floor(totalRows / npts) * npts; % 计算有效行数
        numBlocks = validRows / npts;

        for block = 1:numBlocks
            blockStart = (block - 1) * npts + 1;
            blockEnd = block * npts;

            % 存储到预分配的 cellArray
            for col = 1:expectedCols
                cellArray{col}(:, currentBlockIndex) = Data(blockStart:blockEnd, col);
            end
            currentBlockIndex = currentBlockIndex + 1;
        end
        forProgress();
    end
    forProgress(0);

    % 截断多余的预分配空间
    for col = 1:expectedCols
        cellArray{col} = cellArray{col}(:, 1:(currentBlockIndex - 1)); % 去掉未使用的多余块
    end

    disp('--- 所有文件处理完成 ---');
    disp(['切分后的 cell 数组大小: 1 x ', num2str(length(cellArray))]);
    disp(['每个 cell 包含的矩阵大小: ', num2str(npts), ' x ', num2str(currentBlockIndex - 1)]);
    disp('==========================================');

    % 保存结果
    info = whos('cellArray'); % 获取变量信息      
    if info.bytes <= 2 * 1024^3 % 如果大小小于等于 2GB，执行保存
        save(finalFilePath, 'cellArray');
    end
end
