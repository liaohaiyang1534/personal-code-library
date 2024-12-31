% Interferometry()
%   Interferometry streamflow with various virtual source gathers options
%
%   -- structure
%   AmbiSeis.dt % sampling step
%           .ntrace % trace number of input
%           .npts % sampling length of each segment
%           .numStack % number of split segments
%           .Geometry(ntrace,2) % relative location info for each inter-pair
%           .Offset(ntrace,1) % Offset info for each inter-pair
%           .Trace{ntrace,1} % split time series [npts, numStack] for each trace
%     optionals from preProcflow
%           .procPar
%           .f/.nfft
%
%    procPar.vsIndex, virtual source index option, [num/cn2/cn2n/nxn/ac]
%               n, a scale for one single source and ntrace receivers
%               'cn2', ntrace-1 sources with [vsIndex+1, ntrace] receivers
%               'cn2n', ntrace-1 sources with [vsIndex, ntrace] receivers
%               'nxn', ntrace sources with ntrace receivers
%               'ac', ntrace sources with zero-offset 1 receiver
%           .interfmethod, 'Coherence'  'Correlation'  'Deconvolution'
%           .TWIN, output interferograms time/frequency window [-TWIN TWIN]
%           .tflag, special parameter to control time lag window for output acausal/causal spectrum
%           .tfpresent, 'temporal' for MAPS, spectral for xcorr-spectra, or 'spac' for SPAC
%           .interftimespan, 'acausal+causal', 'acausal', 'causal'
%           .whiteNoise, normalization coefficient for deconvolution
%           .iterationFlag, keep iteration stack matrix or not, default 0 to save space
%           .stackFlag, PWS (1) or linear (0) stacking，default 0
%           .geometry2D, estimate interstation distance using 2d (ll/xy) or 1d ([]) geometry, default 1d
%           .hugeDataFlag, activate huge data option to speed up FFT
%
%   InterfSeis.dt % sampling step
%           .ntrace % trace number of input
%           .npairs % inter-pair numbers of xcorr
%           .npts % sampling length of each xcorr window
%           .numStack % number of split segments
%           .tAxes   % time axes for xcorr
%           .Geometry(ntrace,1) % Offset info for each trace
%           .Shot{i}            % CN2/NxN/AC shot gather
%           .vsIndex % virtual source index
%           .tfpresent % temporal/spectral/spac specific
%           .iterationFlag % store iteration stacking matrix or not, default 0
%
% Usage:
%   InterfSeis = Interferometry(AmbiSeis, procPar)
%
% INPUT:
%   AmbiSeis, noise data structure
%   procPar, input parameters
%
% OUTPUT:
%   InterfSeis, Interferometry data structure
%
% DEPENDENCES:
%   ABdist2D
%   matrixInterf
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 16-Jan-2020
%   replace interftimespan with TWIN to save memory, 05-Feb-2020
%   replace input args with procPar struct, 01-Apr-2020
%   save Offset/Gemoetry info inside InterfSeis, 01-Apr-2020
%   vectorization the code for speed and add parallel option, 01-Apr-2020
%   add cn2/cn2n/nxn/ac virtual source option, 01-Apr-2020
%   output vsIndex/tfpresent to the InterfSeis struct, 01-Apr-2020
%   add df option to control output frequency interval, 02-Apr-2020
%   remove interf_stack initial before parfor, 03-Apr-2020
%   store procPar into output struct for later refer, 16-Apr-2020
%   add hugeDataFlag option to control median results storage, 19-Apr-2020
%       hugeDataFlag == 2 will also reduce FFT points during xcorrtic
%   update InterfSeis geometry with cmp of AmbiSeis geometry, 19-Apr-2020
%   allow input AmbiSeis as spectrum to speedup without fft, 18-Jul-2020
%   remove foutFlag from input proPar of Interferometry, Dec-10-2020
%       1. foutFlag is included in AmbiSeis.procPar if we choose to output spectrum
%       2. it's duplicated and not safe to define two same parameters
%   add pws, Nov-29-2022
%   major revision, Apr-24-2023
%       replace 'triu' in cn2 vsindex with 'tril'
%       the old row/col return from triu is not straightforward (cn2 matrix should be fliplr)
%       the new 'col' means the vs index, the new 'row' means the vr index
%   major revision, Apr-27-2023
%       add selectFlag to allow localselectfunction to implement data select
%
% SEE ALSO:
%   preProcflow
%
% ------------------------------------------------------------------
function InterfSeis = Interferometry(AmbiSeis, procPar)
    % fprintf('-----------------------AmbiSeis Toolbox------------------------------------\n');
    % fprintf('Interferometry method is running ...\n');
    % t0 = tic;
    %
    % vsIndex = procPar.vsIndex; % 1
    interfmethod = procPar.interfmethod; % 选择干涉方法，此处选择'Correlation'
    TWIN = procPar.TWIN; % 干涉时间窗范围，此处选择'4'
    tfpresent = procPar.tfpresent; % 时间窗输出模式，此处选择'temporal'
    interftimespan = procPar.interftimespan; % 控制干涉时间范围，此处选择'acausal+causal'
    whiteNoise = procPar.whiteNoise; % 白噪声归一化系数，此处选择0.5
    %
    if isfield(procPar, 'hugeDataFlag')
        hugeDataFlag = procPar.hugeDataFlag;
    else
        hugeDataFlag = 0;
    end
    %
    numStack = AmbiSeis.numStack;
    npts = AmbiSeis.npts;
    ntrace = AmbiSeis.ntrace;
    dt = AmbiSeis.dt;
    %
    % add df option to control output frequency interval
    % 检查是否存在 df 参数，用于输出频率的控制
    if isfield(procPar, 'df')
        df = procPar.df;
    else
        df = [];
    end
    % 
    if isfield(procPar, 'vsIndex')
        vsIndex = procPar.vsIndex;
    else
        vsIndex = 1;
    end
    %
    if isfield(procPar, 'iterationFlag')
        iterationFlag = procPar.iterationFlag;
    else
        iterationFlag = 0;
    end
    %
    if isfield(procPar, 'tflag')
        tflag = procPar.tflag;
    else
        tflag = [];
    end
    %
    if isfield(procPar, 'selectFlag')
        selectFlag = procPar.selectFlag;
    else
        selectFlag = [];
    end
    %
    % 处理虚拟源 (vsIndex) 配置
    if isnumeric(vsIndex)
        if length(vsIndex)>1
            error('multiple vsIndex has not been supported yet!')
        end
        %     if isvector(vsIndex)
        %         vsIndex_S = vsIndex;
        %     else
        vsIndex_S = vsIndex*ones(ntrace,1);
        %     end
        vsIndex_R = 1:ntrace;
    else
        % multiple virtual sources case
        switch vsIndex
            case 'cn2'  % lower triangle，只取下三角，即对应 ntrace 道的两两组合。
                [row,col]=find(tril(true(ntrace),-1));
            case 'ac'   % diagonal
                [row,col]=find(diag(diag(true(ntrace))));
        end
        %
        vsIndex_S = col;
        vsIndex_R = row;
    end
    % define xcorr geometry
    npairs = length(vsIndex_R); % 道对数量
    %
    Offset = zeros(npairs, 1);
    Geometry = zeros(npairs, 2);
    for i = 1 : npairs
        Geometry(i,:) = (AmbiSeis.Geometry(vsIndex_S(i),:) + AmbiSeis.Geometry(vsIndex_R(i),:))/2; % 计算每个道对的几何中心，两点坐标的平均值
    end
    %
    for i = 1 : npairs
        x1=AmbiSeis.Geometry(vsIndex_S(i),1); y1=AmbiSeis.Geometry(vsIndex_S(i),2);
        x2=AmbiSeis.Geometry(vsIndex_R(i),1); y2=AmbiSeis.Geometry(vsIndex_R(i),2);
        Offset(i) = sqrt((x1-x2).^2 + (y1-y2).^2); % 计算每个道对的偏移量，两点间的欧几里得距离
    end

    % 初始化结果结构体 
    InterfSeis = [];
    if isfield(AmbiSeis, 'Channel')
        InterfSeis.Channel = AmbiSeis.Channel;
    end
    %
    InterfSeis.Geometry = Geometry;
    InterfSeis.Offset = Offset;
    InterfSeis.numStack = numStack;
    InterfSeis.dt = dt;
    InterfSeis.ntrace = ntrace;
    InterfSeis.npairs = npairs;
    InterfSeis.vsIndex = vsIndex;
    InterfSeis.tfpresent = tfpresent;
    %
    % fprintf('>> interfmethod: %s \n', interfmethod);
    % fprintf('>> interftimespan: %s \n', interftimespan);
    % fprintf('>> tfpresent: %s \n', tfpresent);
    % fprintf('>> whiteNoise: %5.2f \n', whiteNoise);
    % initial memory space during the first segment
    % 初始化 uxt 为 npts × ntrace × numStack
    uxt = zeros(npts, ntrace, numStack);
    %
    for i = 1:numStack
        for j = 1 : ntrace
            uxt(:,j,i) = AmbiSeis.Trace{j}(:,i);
        end
    end
    % clear memory
    % AmbiSeis = rmfield( AmbiSeis, 'Trace');
    %
    InterfSeis.StackShot = cell(numStack, 1);
    InterfSeis.Shot = cell(numStack, 1);
    % leave the option to reduce FFT point during xcorr
    if hugeDataFlag == 2
        hugeDataFlagSpeed = 1;
    else
        hugeDataFlagSpeed = 0;
    end
    % stacking flag
    if isfield(procPar, 'stackFlag')
        stackFlag = procPar.stackFlag;
    else
        stackFlag = 0;
    end
    %
    if ~strcmp(tfpresent, 'temporal') && stackFlag>0
        stackFlag = 0;
        warning('tfpresent should be temporal for PWS stacking!');
    end
    % if stackFlag
    %     fprintf('>> temporal stacking: PWS \n');
    % else
    %     fprintf('>> temporal stacking: linear \n');
    % end
    %
    % if ~isempty(selectFlag) && exist('localselectfunction', 'file')
    %     fprintf('>> selective stacking: YES \n');
    % else
    %     fprintf('>> selective stacking: NO \n');
    % end

    % 堆叠过程
    icount = 0;
    % hwait = waitbar(0,'Interferometry IS RUNNING ...');

    forProgress(numStack);

    for i = 1:numStack
        %     waitbar(i/numStack,hwait);
        % fprintf('%d/%d ...\n', i , numStack);
        
        %
        if ~isempty(selectFlag) && exist('s_localselectfunction1', 'file')
            % apply data selection on raw noise segments with custom selective function
            % output the state of the segment, 1 for keep, or 0 for reject
            % 如果用户提供了选择性堆叠文件，则执行
            istate = s_localselectfunction1(uxt(:,:,i),dt,dx,procPar);
            if ~istate
                continue
            end
        end
        icount = icount +1;

        % 调用 matrixInterf_index 函数来计算干涉矩阵
        [interf_matrix, interf_tAxes,errlog] = matrixInterf_index(uxt(:,:,i), vsIndex_S, vsIndex_R, dt,...
            interfmethod, interftimespan, whiteNoise, tfpresent, hugeDataFlagSpeed, df, tflag);
    
        if ~isempty(errlog); error(errlog); end
        %
        if ~isempty(selectFlag) && exist('s_localselectfunction2', 'file')
            % apply data selection on egf segments with custom selective function
            % output the refined matrix, for example, it could be a full-size but zero matrix (hard)
            % or it could be a weighted matrix (soft)
            %
            % interf_matrix = localselectfunction2(interf_matrix, interf_tAxes, tfpresent, selectFlag, istate);
            %
            interf_matrix = s_localselectfunction2(interf_matrix, i, procPar);
        end

        % 数组 interf_tAxes 中查找所有值在区间 [-TWIN, TWIN] 之间
        tIndex = between(-TWIN, TWIN, interf_tAxes, 2);
        %

        if stackFlag > 0 % 如果 stackFlag > 0，则计算相干性（instanPhaseEstimator），否则设置相干性为 1。
            coherency = instanPhaseEstimator(interf_matrix(tIndex, :));
            % elseif stackFlag == 2
            %     coherency = tfphaseEstimator(interf_matrix);
        else
            coherency = 1;
        end

        %
        if icount == 1
            StackShotMatrix = interf_matrix(tIndex, :)*0;
            coherencyStack = interf_matrix(tIndex, :)*0;
        end
        StackShotMatrix = StackShotMatrix + interf_matrix(tIndex, :);
        coherencyStack = coherencyStack + coherency;
        % skip median storage for huge data size
        if hugeDataFlag && i < numStack
            continue
        end
        % optional skip iteration matrix to save memory
        if iterationFlag || i == numStack
            InterfSeis.StackShot{i} = StackShotMatrix;
            InterfSeis.Shot{i} = interf_matrix(tIndex, :);
        end
        forProgress();
    end
    forProgress(0);
    % close(hwait)
    %
    interf_tAxes = interf_tAxes(tIndex); % 仅保留在指定时间窗口内的时间点
    InterfSeis.procPar = procPar;
    InterfSeis.tAxes = interf_tAxes;
    InterfSeis.npts = length(interf_tAxes);
    %
    phaseWeight = power(abs(coherencyStack/numStack), 1);
    InterfSeis.StackShotMatrix = StackShotMatrix.*phaseWeight;
    %
    % totalTime = toc(t0);
    % fprintf('TIME COSTS = %10s sec\n',flt2str(totalTime,3));
    % fprintf('Interferometry method is OVER.\n');

end


%
function [phaseshiftMat] = instanPhaseEstimator(gather)
    % computer the instant phase along each column of the matrix
    % input 2d x-t domain matrix
    % output 2d phase-x matrix
    %
    phiMat = angle(hilbert(gather));
    phaseshiftMat = exp(sqrt(-1)*phiMat);
end

