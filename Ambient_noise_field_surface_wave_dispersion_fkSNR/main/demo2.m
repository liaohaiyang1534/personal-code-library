function demo2(pAmbiSeis, fkprocPar, iprocPar, dx, tracei, currentStart, currentEnd, snrThreshold, time, DispersionPlot, currentTime)
    % 如果 time 是 "all"，直接保留整个 Trace；如果是索引数组，提取指定列
    if ischar(time) && strcmp(time, 'all')
        % 保持原样，无需操作
    elseif isnumeric(time) && ~isempty(time)
        % 提取指定列，并更新 numStack
        pAmbiSeis.Trace = cellfun(@(matrix) matrix(:, time), pAmbiSeis.Trace, 'UniformOutput', false);
        pAmbiSeis.numStack = numel(time);
    else
        error('time 参数无效，请输入 "all" 或一个索引数组');
    end
    
    % 获取调用函数所在的文件夹路径
    stackInfo = dbstack;
    callerFilePath = which(stackInfo(min(numel(stackInfo), 2)).file);
    callingFolderPath = fileparts(callerFilePath);

    % 计算 fkSNR 和 lrSNR
    fprintf('计算 fkSNR :\n');
    numStack = pAmbiSeis.numStack;
    npts = pAmbiSeis.npts;
    ntrace = pAmbiSeis.ntrace;
    dt = pAmbiSeis.dt;
    fkSNR = zeros(numStack, 1);
    lrSNR = zeros(numStack, 1);
    parforProgress(numStack);
    parfor i = 1:numStack
        data = zeros(npts, ntrace);
        for j = 1:ntrace
            data(:,j) = pAmbiSeis.Trace{j}(:,i);
        end
        [fkSNR(i), lrSNR(i)] = s_calfkSNR(data, dt, dx, fkprocPar);
        parforProgress();
    end
    parforProgress(0);

    % 保存 fkSNR 和 lrSNR 的结果
    fullSavePath = generateSavePath(callingFolderPath, 'fkSNR_workspace', tracei, currentStart, currentEnd, time, 'mat', currentTime);
    save(fullSavePath, 'fkSNR', 'lrSNR', 'snrThreshold');

    % 绘制 fkSNR > snrThreshold 图
    xx = 1:numStack;
    fig = figure('Visible', 'off');
    set(fig, 'Position', [100, 100, 900, 300]); % 这里设置宽度为800，高度为600
    plot(xx, fkSNR, 'k.'); % 所有点
    hold on;
    plot(xx(fkSNR > snrThreshold), fkSNR(fkSNR > snrThreshold), 'ro'); % 高于阈值的点
    hold off;

    % 保存 fkSNR > snrThreshold 图
    fullSavePath = generateSavePath(callingFolderPath, 'fkSNR_snrThreshold', tracei, currentStart, currentEnd, time, 'png', currentTime);
    print(fig, fullSavePath, '-dpng', '-r300');
    close(fig);

    % 计算 seismic interferometry
    fprintf('计算 seismic interferometry...\n');
    InterfSeis = Interferometry(pAmbiSeis, iprocPar);
    iprocPar.selectFlag = 1;
    iprocPar.fkSNR = fkSNR;
    iprocPar.lrSNR = lrSNR;
    iprocPar.snrThreshold = snrThreshold;
    pInterfSeis = Interferometry(pAmbiSeis, iprocPar);

    % 保存 InterfSeis 结果
    fullSavePath = generateSavePath(callingFolderPath, 'InterfSeis_workspace', tracei, currentStart, currentEnd, time, 'mat', currentTime);
    save(fullSavePath, 'pAmbiSeis', 'InterfSeis', 'pInterfSeis');

    % 绘制 virtual source gather 图并保存
    [uxt_stack1, x_stack, t] = generateAndSaveVirtual(InterfSeis, callingFolderPath, 'virtual_source_gather_allStacking', ...
                        tracei, currentStart, currentEnd, time, 'png', currentTime);
    [uxt_stack2] = generateAndSaveVirtual(pInterfSeis, callingFolderPath, 'virtual_source_gather_fkSNRSelectiveStacking', ...
                        tracei, currentStart, currentEnd, time, 'png', currentTime);
    
    % 绘制 wiggle super gather 图并保存
    generateAndSaveWiggle(x_stack, t, uxt_stack1, uxt_stack2, callingFolderPath, 'wiggle_super_gather', tracei, currentStart, currentEnd, time, 'png', currentTime)

    % 绘制 dispersion energy 图并保存
    % dispersion energy绘图参数
    tindex = between(0, 2, t,2);
    fmin = DispersionPlot.fmin;
    fmax = DispersionPlot.fmax;
    vmin = DispersionPlot.vmin;
    vmax = DispersionPlot.vmax;
    [fv1,f,v] = FPhaseshift(uxt_stack1(tindex, :), x_stack, t(tindex), 1, fmin, fmax, vmin, vmax, 0);
    [fv2] = FPhaseshift(uxt_stack2(tindex, :), x_stack, t(tindex), 1, fmin, fmax, vmin, vmax, 0);
    generateAndSaveDispersion(f, v, fv1, fv2, callingFolderPath, 'dispersion_energy', tracei, currentStart, currentEnd, time, 'png', currentTime);

    % 保存 fkSNR stack 结果
    fullSavePath = generateSavePath(callingFolderPath, 'fkSNR_stack', tracei, currentStart, currentEnd, time, 'mat', currentTime);
    save(fullSavePath, 'f', 'v', 'fv2');
end
  
    
% 辅助函数：生成文件保存路径
function fullSavePath = generateSavePath(baseFolder, filePrefix, tracei, currentStart, currentEnd, time, extension, currentTime)
    % 定义主文件夹名称
    outputFolderName = ['output_', currentTime];
    baseFolder = fullfile(baseFolder, outputFolderName);
    
    % 确保主文件夹存在
    if ~exist(baseFolder, 'dir')
        mkdir(baseFolder);
    end
    
    % 子文件夹名称也是文件前缀
    subFolderName = filePrefix;

    % 确保子文件夹存在
    newFolderPath = fullfile(baseFolder, subFolderName);
    if ~exist(newFolderPath, 'dir')
        mkdir(newFolderPath);
    end

    % 根据 time 动态生成字符串
    if ischar(time) && strcmp(time, 'all')
        timeStr = 'all';
    elseif isnumeric(time) && ~isempty(time)
        timeStr = sprintf('%d-%d', min(time), max(time));
    else
        error('time 参数无效，请输入 "all" 或一个索引数组');
    end

    % 生成文件名
    fileName = sprintf('%s_surveyLine(%d)_Start(%d)_End(%d)_Time(%s).%s', ...
                        filePrefix, tracei, currentStart, currentEnd, timeStr, extension);

    % 生成完整保存路径
    fullSavePath = fullfile(newFolderPath, fileName);
end


% 辅助函数：绘制 virtual source gather 图并保存
function  [uxt_stack, x_stack, t] = generateAndSaveVirtual(InterfSeis, folderPath, baseName, tracei, currentStart, currentEnd, time, ext, currentTime)
    % 生成保存路径
    fullSavePath = generateSavePath(folderPath, baseName, tracei, currentStart, currentEnd, time, ext, currentTime);    
    
    % 创建一个不可见的图像窗口
    fig = figure('Visible', 'off');

    % 获取数据
    t = InterfSeis.tAxes;           % 时间轴
    x = InterfSeis.Offset;          % 空间偏移
    numIndex = InterfSeis.numStack; % 堆叠索引
    uxt = InterfSeis.StackShot{numIndex}; % 数据矩阵

    % 对每列归一化
    uxt = bsxfun(@rdivide, uxt, max(abs(uxt), [], 1));

    iprocPar = InterfSeis.procPar;
    if strcmp(iprocPar.vsIndex, 'cn2')
        %
        [uxt_stack, x_stack] = copstacking(uxt,x);

    else
        uxt_stack = uxt;
        x_stack = x;
    end

    % 绘制图像
    h = imagesc(x, t, uxt);

    % 设置图像数据映射和透明度
    set(h, 'CDataMapping', 'scaled');
    set(h, 'alphadata', ~isnan(uxt));

    % 设置颜色映射为 jet，并翻转 y 轴
    colormap(gca, jet);
    axis ij;

    % 设置坐标轴标签
    xlabel('Offset (m)');
    ylabel('Time (sec)');

    % 保存图像
    print(fig, fullSavePath, '-dpng', '-r300');

    % 关闭窗口
    close(fig);
end

% 辅助函数：绘制 wiggle super gather 图并保存
function generateAndSaveWiggle(x, t, uxt1, uxt2, folderPath, filePrefix, tracei, currentStart, currentEnd, time, extension, currentTime)
    % 生成完整的保存路径
    fullSavePath = generateSavePath(folderPath, filePrefix, tracei, currentStart, currentEnd, time, extension, currentTime);
    
    % 对输入数据按列进行归一化
    uxt1 = bsxfun(@rdivide, uxt1, max(abs(uxt1), [], 1)); % 归一化第一个 Wiggle 数据
    uxt2 = bsxfun(@rdivide, uxt2, max(abs(uxt2), [], 1)); % 归一化第二个 Wiggle 数据

    % 创建不可见的图形窗口
    fig = figure('Visible', 'off'); % 设置图形窗口不可见
    set(fig, 'Units', 'pixels', 'Position', [100, 100, 900, 1200]); % 设置窗口位置和大小（以像素为单位）
    
    % 绘制第一个子图
    subplot(1, 2, 1); % 创建第一个子图
    wigb(uxt1, x, t, 'k'); % 绘制第一个 Wiggle 图
    box on; % 添加边框
    set(gca, 'XAxisLocation', 'bottom'); % 设置 X 轴位置
    xlabel('Offset (m)'); % 设置 X 轴标签
    ylabel('Time (sec)'); % 设置 Y 轴标签
    title('All Stack'); % 设置标题
    ylim([0 1]); % 设置 Y 轴范围
    
    % 绘制第二个子图
    subplot(1, 2, 2); % 创建第二个子图
    wigb(uxt2, x, t, 'k'); % 绘制第二个 Wiggle 图
    box on; % 添加边框
    set(gca, 'XAxisLocation', 'bottom'); % 设置 X 轴位置
    xlabel('Offset (m)'); % 设置 X 轴标签
    ylabel('Time (sec)'); % 设置 Y 轴标签
    title('fkSNR Stack'); % 设置标题
    ylim([0 1]); % 设置 Y 轴范围
    
    % 保存图像到文件
    print(fig, fullSavePath, '-dpng', '-r300'); % 保存为高分辨率 PNG 文件
    
    % 关闭图形窗口，释放内存
    close(fig);

end


% 辅助函数：绘制 dispersion spectra 图并保存
function generateAndSaveDispersion(f, v, fv1, fv2, folderPath, filePrefix, tracei, currentStart, currentEnd, time, extension, currentTime)
    % 对两个二维矩阵分别进行按列归一化处理
    fv1 = bsxfun(@rdivide, fv1, max(abs(fv1), [], 1)); % 第一个子图数据归一化
    fv2 = bsxfun(@rdivide, fv2, max(abs(fv2), [], 1)); % 第二个子图数据归一化
    
    % 生成完整的保存路径
    fullSavePath = generateSavePath(folderPath, filePrefix, tracei, currentStart, currentEnd, time, extension, currentTime);
    
    % 创建不可见的图形窗口
    fig = figure('Visible', 'off'); % 设置图形窗口不可见
    set(fig, 'Units', 'normalized', 'Position', [0.2 0.2 0.8 0.4]); % 可选：设置窗口大小和位置
    
    % 绘制第一个子图
    subplot(1, 2, 1); % 创建第一个子图
    imagesc(f, v, fv1); % 绘制二维色散图
    dspfig=imagesc(f,v,fv1);
    set(dspfig,'CDataMapping','scaled') ; % 设置颜色映射
    colormap(gca, "turbo"); % 设置颜色图
    set(dspfig, 'alphadata', ~isnan(fv1)); % 处理 NaN 数据的透明显示
    axis xy; % 设置轴方向
    xlabel('Frequency (Hz)'); % 设置 X 轴标签
    ylabel('Phase velocity (m/s)'); % 设置 Y 轴标签
    title('All Stack'); % 设置标题
    
    % 绘制第二个子图
    subplot(1, 2, 2); % 创建第二个子图
    imagesc(f, v, fv2); % 绘制二维色散图
    dspfig=imagesc(f,v,fv2);
    set(dspfig,'CDataMapping','scaled') ; % 设置颜色映射
    colormap(gca, "turbo"); % 设置颜色图
    set(dspfig, 'alphadata', ~isnan(fv2)); % 处理 NaN 数据的透明显示
    axis xy; % 设置轴方向
    xlabel('Frequency (Hz)'); % 设置 X 轴标签
    ylabel('Phase velocity (m/s)'); % 设置 Y 轴标签
    title('fkSNR Stack'); % 设置标题
    
    % 保存图像到文件
    print(fig, fullSavePath, '-dpng', '-r300'); % 保存为高分辨率 PNG 文件
    
    % 关闭图形窗口，释放内存
    close(fig);

end
