function AmbiSeis = generateAmbiSeisFromSGY(cellArray, npts, dx, samplingInterval)
    % generateAmbiSeisFromSGY: 生成 AmbiSeis 结构，Trace 数据来源于 processAndSplitSGYFiles
    % 输入参数：
    %   npts - 每个块的行数
    % 输出参数：
    %   AmbiSeis - 生成的 AmbiSeis 结构体

    % 获取 numStack, ntrace 的信息
    numStack = size(cellArray{1}, 2); % 每块的列数 (k)
    ntrace = length(cellArray);       % 跟踪数量 (列数)

    % % 构造 procPar 参数
    % procPar.t1t2 = [0, 1000];        % 时间范围
    % procPar.format = 'fcnt';         % 格式类型
    % procPar.eventLen = 20;           % 事件长度
    % procPar.numStack = numStack;     % 叠加次数
    % procPar.overLap = 0.8;           % 重叠率
    % procPar.dx = 1;                  % 间隔信息
    % procPar.geometryInfo = [];       % 几何信息
    % procPar.channelno = 3;           % 通道编号
    % procPar.wrtFlag = 0;             % 写入标志

    procPar.filtertype = 'bp';
    procPar.f1 = 0.5;
    procPar.f2 = 60;
    procPar.Taperwidth = 0.05;
    procPar.Tapertype = 'hann';
    procPar.tdnormtype = 'ram';
    procPar.FreqWind2d = [];
    procPar.narrowdf = [];
    procPar.fdnormtype = 'ram';
    procPar.debug = 0;
  
    % 构造 Geometry 参数
    zero_col = zeros(ntrace, 1);     
    Geometry = [(1:ntrace)', zero_col]* dx;   

    % 构造 AmbiSeis 结构体
    AmbiSeis.ntrace = ntrace;        % 跟踪数量
    AmbiSeis.Channel = 'Vertical';   % 通道信息
    AmbiSeis.Geometry = Geometry;    % 几何数据
    AmbiSeis.Trace = cellArray;      % 跟踪数据
    AmbiSeis.dt = samplingInterval;  % 时间间隔 (秒)
    AmbiSeis.npts = npts;            % 数据点数
    AmbiSeis.numStack = numStack;    % 叠加次数
    AmbiSeis.procPar = procPar;      % 处理参数

    % % 打印结果信息
    % disp('AmbiSeis 结构已生成！');
end
