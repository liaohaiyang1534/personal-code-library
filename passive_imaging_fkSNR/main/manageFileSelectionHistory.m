function [selectedRecord, historyFilePath] = manageFileSelectionHistory(fileExtension)
    % 文件选择历史管理工具
    %
    % 输入:
    % - fileExtension (必选): 文件扩展名，用于筛选特定类型的文件，例如 'txt' 或 'jpg'。
    %
    % 输出:
    % - selectedRecord: 用户最终选择的记录，包含以下字段：
    %   - pathName: 所选文件所在的文件夹路径。
    %   - fileNames: 所选文件的文件名列表。
    %   - timeStamp: 记录创建的时间戳，格式为 'yyyy-MM-dd HH:MM:SS'。
    % - historyFilePath (可选): 历史记录文件的完整路径。
    
    % 功能说明:
    % 1. 加载或初始化历史记录:
    %    - 历史记录文件名根据调用此函数的 .m 文件所在目录动态生成。
    %    - 若文件存在，则加载历史记录；否则初始化为固定 20 条空记录。
    % 2. 显示主界面:
    %    - 显示文件选择历史记录及相关操作选项。
    %    - 支持用户选择记录、查看记录详情、收藏记录或删除记录。
    %    - 用户可以选择新文件并自动更新历史记录。
    % 3. 动态更新历史记录:
    %    - 用户操作后，程序自动更新历史记录文件，并刷新主界面显示。
    %
    % 使用示例:
    % - 1.筛选扩展名为 'txt' 的文件：
    % - selectedRecord = manageFileSelectionHistory('txt');
    %
    % - 2.筛选扩展名为 'jpg' 的文件及历史文件路径:
    %   [selectedRecord, historyFilePath] = manageFileSelectionHistory('jpg');
    %
    % 主要交互流程:
    % 1. 启动文件选择历史管理界面，加载或初始化历史记录。
    % 2. 用户通过界面选择文件或历史记录，执行查看、收藏、删除等操作。
    % 3. 确认操作后，返回所选记录，并自动更新历史记录文件
    
    % 生成唯一的历史记录文件名
    stackInfo = dbstack;
    if numel(stackInfo) > 1
        % 如果是被其他文件调用
        callerFilePath = which(stackInfo(2).file);
    else
        % 如果是直接运行的文件
        callerFilePath = which(stackInfo(1).file);
    end

    % 获取调用文件所在的文件夹路径和文件名
    [callingFolderPath, callerFileName, ~] = fileparts(callerFilePath); % 获取路径和文件名
    [~, folderName] = fileparts(callingFolderPath); % 获取文件夹名

    % 定义历史记录文件名，格式：selectionHistory_<文件夹名>_<调用者文件名>_<拓展名>.mat
    historyFilePath = fullfile(callingFolderPath, sprintf('selectionHistory_%s_%s_%s.mat', folderName, callerFileName, fileExtension));

    % 加载选择记录
    if exist(historyFilePath, 'file')
        load(historyFilePath, 'selectionHistory'); % 加载历史记录
    else
        % 初始化空记录，固定为 20 个
        emptyRecord = struct('pathName', '', 'fileNames', {{}}, 'timeStamp', '', 'isFavorite', 0);
        selectionHistory(1:20) = emptyRecord; % 初始化 20 条空记录
    end

    % 确保执行时间字段格式正确
    for i = 1:numel(selectionHistory)
        if isempty(selectionHistory(i).timeStamp)
            selectionHistory(i).timeStamp = ''; % 确保字段存在且为字符串
        end
    end

    % 创建主界面
    fig = uifigure('Name', sprintf('%s 文件选择历史管理', fileExtension), 'Position', [300, 300, 1100, 670]);
    
    % 将 fileExtension 存储到 UserData
    fig.UserData = struct('selectedRecord', [], 'fileExtension', fileExtension);

    % 创建主窗口布局
    grid = uigridlayout(fig, [11, 2]); % 2 列 × 10 行
    grid.RowHeight = repelem({50}, 11); % 每行固定高度为 50
    grid.ColumnWidth = {'1x', '1x'}; % 两列等宽

    % 界面标题
    titleLabel = uilabel(grid, 'Text', sprintf('%s 文件选择工具', fileExtension), ...
        'HorizontalAlignment', 'center', 'FontSize', 20, 'FontWeight', 'bold');
    titleLabel.Layout.Row = 1;
    titleLabel.Layout.Column = [1, 2];

    % 动态刷新主界面内容
    refreshMainWindow(fig, selectionHistory, historyFilePath, fileExtension);

    % 等待用户操作
    uiwait(fig);

    % 返回选中的记录
    if isvalid(fig)
        selectedRecord = fig.UserData.selectedRecord;
        close(fig);
    else
        selectedRecord = [];
    end
end

function showRecordDetails(parentFig, selectionHistory, recordIndex, historyFilePath)
    detailFig = uifigure('Name', '文件详情', 'Position', [150, 150, 520, 300]);

    % 提取完整文件路径
    filePath = selectionHistory(recordIndex).pathName;
    
    % 保留根目录和最后的文件夹名
    [pathRoot, lastFolder] = fileparts(filePath);
    [pathRoot, ~] = fileparts(pathRoot);
    
    % 提取中间路径部分
    middlePath = extractBetween(filePath, [pathRoot '\'], ['\' lastFolder]);
    
    % 折叠显示路径
    if length(filePath) > 50
        filePathDisplay = [pathRoot, '\...', '\', lastFolder];
    else
        filePathDisplay = filePath;
    end
    
    % 显示路径
    pathLabel = uilabel(detailFig, 'Text', sprintf('路径: %s', filePathDisplay), ...
        'Position', [20, 260, 560, 20], 'FontSize', 12, 'HorizontalAlignment', 'left');

    % 设置鼠标悬停显示中间路径部分
    if ~isempty(middlePath)
        pathLabel.Tooltip = sprintf('折叠路径中间部分: %s', middlePath{1});
    else
        pathLabel.Tooltip = '折叠路径中间部分为空';
    end

    % 文件名列表标题
    uilabel(detailFig, 'Text', '文件名列表:', 'Position', [20, 240, 200, 20], 'FontSize', 12);

    % 文件名列表
    uilistbox(detailFig, 'Items', selectionHistory(recordIndex).fileNames, ...
        'Position', [20, 65, 480, 170], 'FontSize', 11);

    % 按钮宽度和间距
    buttonWidth = 140;
    buttonHeight = 30;
    buttonSpacing = 30;
    startX = 20; % 第一个按钮的起始位置
    startY = 20; % 按钮的 Y 位置

    % 添加“选择该记录”按钮
    uibutton(detailFig, 'Text', '选择该记录', ...
        'Position', [startX, startY, buttonWidth, buttonHeight], ...
        'ButtonPushedFcn', @(btn, event) selectRecord(parentFig, detailFig, selectionHistory(recordIndex)), ...
        'BackgroundColor', [0.9, 0.9, 1]);

    % 收藏或取消收藏按钮
    if isfield(selectionHistory(recordIndex), 'isFavorite') && selectionHistory(recordIndex).isFavorite
        % 取消收藏按钮
        uibutton(detailFig, 'Text', '取消收藏', ...
            'Position', [startX + buttonWidth + buttonSpacing, startY, buttonWidth, buttonHeight], ...
            'ButtonPushedFcn', @(btn, event) toggleFavorite(recordIndex, false, historyFilePath, detailFig, parentFig), ...
            'BackgroundColor', [0.9, 0.9, 1]);
    else
        % 收藏按钮
        uibutton(detailFig, 'Text', '收藏', ...
            'Position', [startX + buttonWidth + buttonSpacing, startY, buttonWidth, buttonHeight], ...
            'ButtonPushedFcn', @(btn, event) toggleFavorite(recordIndex, true, historyFilePath, detailFig, parentFig), ...
            'BackgroundColor', [0.9, 0.9, 1]);
    end
    
    % 删除按钮
    uibutton(detailFig, 'Text', '删除', ...
        'Position', [startX + 2 * (buttonWidth + buttonSpacing), startY, buttonWidth, buttonHeight], ...
        'ButtonPushedFcn', @(btn, event) deleteRecord(recordIndex, historyFilePath, detailFig, parentFig), ...
        'BackgroundColor', [0.9, 0.9, 1]);
end


function selectRecord(parentFig, detailFig, record)
    % 移除 isFavorite 字段并将记录设为当前选择
    if isfield(record, 'isFavorite')
        record = rmfield(record, 'isFavorite');
    end
    parentFig.UserData.selectedRecord = record;
    uiresume(parentFig);
    close(detailFig);
end

function toggleFavorite(recordIndex, isFavorite, historyFilePath, detailFig, parentFig)
    % 从 parentFig.UserData 获取 fileExtension
    fileExtension = parentFig.UserData.fileExtension;

    % 加载历史记录文件
    if exist(historyFilePath, 'file')
        load(historyFilePath, 'selectionHistory');
    else
        error('历史记录文件不存在，无法更新收藏状态。');
    end

    % 更新对应记录的收藏状态
    selectionHistory(recordIndex).isFavorite = isFavorite;

    % 保存更新后的历史记录
    save(historyFilePath, 'selectionHistory');

    % 关闭详细窗口
    close(detailFig);

    % 动态刷新主界面内容
    refreshMainWindow(parentFig, selectionHistory, historyFilePath, fileExtension);
end

function deleteRecord(recordIndex, historyFilePath, detailFig, parentFig)
    % 从 parentFig.UserData 获取 fileExtension
    fileExtension = parentFig.UserData.fileExtension;

    % 加载历史记录文件
    if exist(historyFilePath, 'file')
        load(historyFilePath, 'selectionHistory');
    else
        error('历史记录文件不存在，无法删除记录。');
    end

    % 重置指定记录为默认值
    selectionHistory(recordIndex).pathName = '';
    selectionHistory(recordIndex).fileNames = {};
    selectionHistory(recordIndex).timeStamp = '';
    selectionHistory(recordIndex).isFavorite = 0;

    % 保存更新后的历史记录
    save(historyFilePath, 'selectionHistory');

    % 关闭详细窗口
    close(detailFig);

    % 动态刷新主界面
    refreshMainWindow(parentFig, selectionHistory, historyFilePath, fileExtension);
end

function selectedRecord = selectNewFiles(fig, historyFilePath, selectionHistory, fileExtension, recordIndex) 
  
    % 打开文件选择对话框
    [fileNames, pathName] = uigetfile(fileExtension, '选择文件', 'MultiSelect', 'on');
    if isequal(fileNames, 0) % 用户取消选择，返回空记录
        selectedRecord = [];
        return;
    end
    if ~iscell(fileNames), fileNames = {fileNames}; end

    % 创建新记录
    newRecord.pathName = pathName;
    newRecord.fileNames = fileNames;
    newRecord.timeStamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    newRecord.isFavorite = 0; % 初始化 isFavorite 为 0

    % 保存到指定位置的历史记录
    selectionHistory(recordIndex) = newRecord;

    % 保存更新后的历史记录到文件
    save(historyFilePath, 'selectionHistory');

    % 设置输出的 selectedRecord，仅包含所需字段
    selectedRecord = rmfield(newRecord, 'isFavorite'); % 移除 isFavorite 字段

    % 更新界面的选中记录
    fig.UserData.selectedRecord = selectedRecord;

    % 恢复界面
    uiresume(fig);
end

function refreshMainWindow(fig, selectionHistory, historyFilePath, fileExtension)
    % 获取主界面布局
    grid = fig.Children; % 获取网格布局对象

    % 清除当前的历史记录按钮
    delete(allchild(grid));

    % 重新绘制界面标题
    titleLabel = uilabel(grid, 'Text', sprintf('%s 文件选择工具', fileExtension), ...
        'HorizontalAlignment', 'center', 'FontSize', 20, 'FontWeight', 'bold');
    titleLabel.Layout.Row = 1;
    titleLabel.Layout.Column = [1, 2];

    % 动态生成按钮（固定为 20 条记录，以 2 列布局）
    for i = 1:20
        row = floor((i - 1) / 2) + 2; % 从第 2 行开始
        col = mod(i - 1, 2) + 1; % 第 1 列或第 2 列

        if ~isempty(selectionHistory(i).pathName)
            % 如果有记录，生成按钮标签内容
            folderName = selectionHistory(i).pathName; % 获取文件夹名
            if endsWith(folderName, '\') || endsWith(folderName, '/')
                folderName = folderName(1:end-1); % 移除最后的斜杠
            end
            
            % 截取文件夹名称，如果超过 12 个字符，截断并追加“……”
            [~, folderName] = fileparts(folderName); % 提取文件夹名称
            if length(folderName) > 12
                % 超过长度则从右向左截断并添加省略号
                folderName = ['……', folderName(end-11:end)]; % 从右截取最后12个字符，并添加省略号在前
            else
                % 不足长度用空格补齐（左对齐）
                folderName = sprintf('%-14s', folderName); % 左对齐补齐到 14 个字符
            end

            % 格式化执行时间为 月-日-时-分钟
            fullTimeStamp = selectionHistory(i).timeStamp; % 原始时间戳
            formattedTime = datestr(datenum(fullTimeStamp, 'yyyy-mm-dd HH:MM:SS'), 'yyyy-mm-dd HH:MM'); % 转换格式

            % 按钮标签内容
            buttonLabel = sprintf('[%02d] 执行时间: %s 文件夹名: %s 文件数: %d', ...
                                  i, formattedTime, folderName, ...
                                  numel(selectionHistory(i).fileNames));

            % 设置背景颜色：浅红色（收藏）或默认灰色
            if isfield(selectionHistory(i), 'isFavorite') && selectionHistory(i).isFavorite
                bgColor = [1, 0.8, 0.8]; % 浅红色背景（收藏）
            else
                bgColor = [0.9, 0.9, 0.9]; % 默认灰色背景
            end

            % 创建显示记录信息的按钮
            recordButton = uibutton(grid, ...
                'Text', buttonLabel, ...
                'ButtonPushedFcn', @(btn, event) showRecordDetails(fig, selectionHistory, i, historyFilePath), ...
                'FontSize', 13, ...
                'HorizontalAlignment', 'left', ...
                'FontName', 'Courier New', ...
                'FontWeight', 'bold', ...
                'FontColor', [0, 0, 0], ...
                'BackgroundColor', bgColor);
            recordButton.Layout.Row = row;
            recordButton.Layout.Column = col;
        else
            % 如果没有记录，显示占位按钮，支持选择新文件
            placeholderButton = uibutton(grid, ...
                'Text', sprintf('[%02d] 选择新文件', i), ...
                'FontSize', 11, ...
                'HorizontalAlignment', 'left', ...
                'FontName', 'Courier New', ...
                'FontColor', [0.6, 0.6, 1], ...
                'BackgroundColor', [0.9, 0.9, 0.9], ...
                'ButtonPushedFcn', @(btn, event) selectNewFiles(fig, historyFilePath, selectionHistory, strcat('*.', fileExtension), i));
            placeholderButton.Layout.Row = row;
            placeholderButton.Layout.Column = col;
        end
    end
end
