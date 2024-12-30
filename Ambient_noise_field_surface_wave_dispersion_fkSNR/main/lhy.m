clc
clear

currentTime = datestr(now, 'YYYYmmdd_HHMMSS'); % 获取当前时间字符串

RollingParams.traceStartEnd = [
    % 测线首尾道号
    % 210   350;
    % 355   430;
    % 440   570;
    % 575   695;
    % 700   714;
    138 198;
];  


% ---------------------------------------------------------


fmin = 1;
fmax = 50;
vmin = 10;
vmax = 600;

dx = 0.5; % channel spacing(m)
dt = 0.01; % sampling (s)

segment = 5; % every time segment into the struct Ambientseis(s)
npts = segment/dt;


% ---------------------------------------------------------


array_length = 30; % array length (m)
array_step = 10; % array step when finishing whole survey line (m)

snrThreshold = 1.6; % depend on certain data to choose better segment noise

array_channel_number = array_length / dx;
array_channel_step = array_step / dx;

% ---------------------------------------------------------

% 定义输入点
poly1_points = [
    0.0, 0.0;
    20, 0.1;
    20, 0.06;
];

poly2_points = [
    0.0, 0.0;
    20, 0.06;
    20, 0.0;
];

poly_points = [
    0.0, 0.002;
    0.0, 0.004;
    20, 0.1;
    40, 0.1;
];


plot_poly = 0; % 1 表示绘制多边形，0 表示不绘制

points_num = 425; % to decide polys' numbers, no need to change in general


% ---------------------------------------------------------


% iprocPar = generateIprocPar(); % iprocPar 结构体定义，!!!函数内部需要修改参数!!!
% 初始化结构体
iprocPar = struct();
% 定义字段及其默认值
iprocPar.vsIndex = 'cn2';                           
iprocPar.interfmethod = 'Coherence';                
iprocPar.interftimespan = 'acausal+causal';         
iprocPar.whiteNoise = 0.5;                          
iprocPar.tfpresent = 'temporal';                    
iprocPar.TWIN = 1;                                  
iprocPar.paralFlag = 0;                             
iprocPar.iterationFlag = 0;  


% 生成多边形数据
poly1 = generatePolygon(poly1_points, points_num);
poly2 = generatePolygon(poly2_points, points_num);
poly = generatePolygon(poly_points, points_num);

fkprocPar.fmin = fmin;
fkprocPar.fmax = fmax;
fkprocPar.vmin = vmin;
fkprocPar.vmax = vmax;
fkprocPar.poly = poly;
fkprocPar.poly1 = poly1;
fkprocPar.poly2 = poly2;
fkprocPar.fkSNRplt = 1; % polt choice: 1 or 0


RollingParams.npts = npts;                    % 分段采样长度
RollingParams.offset = dx;                  % 道间距
RollingParams.samplingInterval = dt;      % 采样间隔(s)
RollingParams.windowLength = array_channel_number;            % 排列长度
RollingParams.stepSize = array_channel_step;                 % 排列步进
RollingParams.snrThreshold = snrThreshold;           % SNR阈值
RollingParams.time = 'all';                   % 时间段(RollingParams.time = 'all'或者 3：39)


% dispersion energy频散图，绘图用参数!!!函数内部需要修改参数!!!
DispersionPlot.fmin = fmin;
DispersionPlot.fmax = fmax;
DispersionPlot.vmin = vmin;
DispersionPlot.vmax = vmax;


if plot_poly ==1
    % 可视化多边形
    figure;
    fill(poly1(:, 1), poly1(:, 2), 'r', 'FaceAlpha', 0.5, 'DisplayName', 'poly1'); hold on;
    fill(poly2(:, 1), poly2(:, 2), 'g', 'FaceAlpha', 0.5, 'DisplayName', 'poly2');
    fill(poly(:, 1), poly(:, 2), 'b', 'FaceAlpha', 0.5, 'DisplayName', 'poly');
    title('Interpolated Polygons');
    xlabel('X-Axis');
    ylabel('Y-Axis');
    legend('show');
    
    % 设置网格线
    grid on; % 显示网格
    
    % 添加次网格线，设置主要和次要网格线的细度和透明度
    ax = gca; % 获取当前坐标轴
    ax.XMinorTick = 'on'; % 开启 x 轴次刻度
    ax.YMinorTick = 'on'; % 开启 y 轴次刻度
    
    ax.MinorGridLineStyle = '-'; % 次网格线样式
    ax.MinorGridColor = [0.5 0.5 0.5]; % 次网格线颜色
    ax.MinorGridAlpha = 0.3; % 次网格线透明度，范围从 0（完全透明）到 1（不透明）
    % 选择性地保持比例
    % axis equal; % 保持比例
    ax.GridLineStyle = '-'; % 主网格线样式
    ax.GridAlpha = 0.7; % 主网格线透明度，调整为合适的值
end


% 调用 processAndSplitSGYFiles 函数获取 Trace 数据
cellArray = processAndSplitSGYFiles('sgy', RollingParams.npts);
% load('AmbiSeis_demo2.mat');

% 滑动窗口截取优化
numTraces = size(RollingParams.traceStartEnd, 1); % 获取测线数目

% 初始化窗口数量的记录数组
windowCounts = zeros(numTraces, 1);

% 循环处理每条测线
for tracei = 1:numTraces
    % 提取当前测线的起点和终点
    startVal = RollingParams.traceStartEnd(tracei, 1); % 当前测线首道号
    endVal = RollingParams.traceStartEnd(tracei, 2);   % 当前测线尾道号

    % 仅在第 1 条测线打印 "开始处理测线"
    if tracei == 1
        fprintf('-------------- 开始处理测线 %d --------------\n', tracei);
    end

    % 提前计算当前测线的窗口数量
    numWindows = floor((endVal - startVal - RollingParams.windowLength) / RollingParams.stepSize) + 1;
    windowCounts(tracei) = max(numWindows, 0); % 确保窗口数量为非负值

    % 打印预测窗口数量
    fprintf('测线 %d 预计窗口数量: %d\n', tracei, windowCounts(tracei));

    % 计算总任务数的最大宽度（用于空格补齐，单独针对当前测线）
    totalTasksWidth = floor(log10(windowCounts(tracei))) + 1; % 当前测线任务数的宽度

    % 初始化当前起点
    currentStart = startVal;
    currentWindowIndex = 0; % 当前窗口索引

    % 滑动窗口截取
    while currentStart + RollingParams.windowLength <= endVal
        % 更新窗口索引
        currentWindowIndex = currentWindowIndex + 1;

        % 计算窗口的终点
        currentEnd = currentStart + RollingParams.windowLength;

        % 确保索引对齐显示（按测线自己的总任务数对齐）
        progressStr = sprintf(['%', num2str(totalTasksWidth), 'd/%', num2str(totalTasksWidth), 'd'], ...
                               currentWindowIndex, windowCounts(tracei));

        % 显示窗口的起点和终点，以及执行进度
        fprintf('----------- 测线 %d 执行任务: %s -----------\n', ...
                tracei, progressStr);
        fprintf('测线 %d: 窗口起点 = %d, 窗口终点 = %d\n', tracei, currentStart, currentEnd);

        % AmbiSeisTemp 结构体定义
        cellArrayTemp = cellArray(currentStart: currentEnd);
        AmbiSeisTemp = generateAmbiSeisFromSGY(cellArrayTemp, RollingParams.npts, RollingParams.offset, RollingParams.samplingInterval); % !!!函数内部需要修改参数!!!

        % ---------------------------------------------------------
        
        npts = AmbiSeisTemp.npts;
        ntrace = AmbiSeisTemp.ntrace;
        dt = AmbiSeisTemp.dt;

        data = zeros(npts, ntrace);
        for j = 1 : ntrace
            data(:,j) = AmbiSeisTemp.Trace{j}(:,10);
        end
        [~,~,filterin,filterin1,filterin2] = s_calfkSNR(data,dt,dx,fkprocPar);
        fkprocPar.filterin = filterin;
        fkprocPar.filterin1 = filterin1;
        fkprocPar.filterin2 = filterin2;
        fkprocPar.fkSNRplt = 0;

        % ---------------------------------------------------------

        % 调用处理函数
        demo2(AmbiSeisTemp, fkprocPar, iprocPar, RollingParams.offset, tracei, currentStart, currentEnd, RollingParams.snrThreshold, RollingParams.time, DispersionPlot, currentTime);

        % 滑动窗口
        currentStart = currentStart + RollingParams.stepSize;

        % 每个窗口之间打印分隔符，但不在最后一个窗口打印
        if currentStart + RollingParams.windowLength <= endVal
            disp('------------------------------------------');
        end
    end

    % 打印分隔符（合并完成和开始信息）
    if tracei < numTraces
        % 非最后一个测线时
        fprintf('======= 完成处理测线 %d，开始处理测线 %d =======\n', tracei, tracei + 1);
    else
        % 最后一个测线时
        fprintf('============== 完成处理测线 %d ==============\n', tracei);
    end
end