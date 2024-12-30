function percent = parforProgress(N)
    % parfor 并行任务进度监控工具
    %
    % 功能说明:
    % 1. 初始化任务进度:
    %    - 调用 'parforProgress(N)' 创建进度文件 'parforProgress.txt'。
    %    - 记录任务总数和任务开始时间。
    %    - 显示初始进度条，任务进度为 0%。
    % 2. 动态更新任务进度:
    %    - 在 'parfor' 循环内，每次任务完成时调用 'parforProgress()'。
    %    - 自动记录已完成任务数，计算完成百分比、已运行时间及预计剩余时间。
    %    - 动态显示实时任务进度条和任务信息。
    % 3. 完成任务清理:
    %    - 调用 'parforProgress(0)' 删除进度文件，并显示完整任务进度。
    %    - 计算并显示总运行时间。
    %
    % 使用示例:
    % % 假设任务总数为 N
    % parforProgress(N); % 初始化任务进度
    % parfor i = 1:N
    %     pause(0.1); % 模拟任务执行
    %     parforProgress(); % 每次任务完成后更新进度
    % end
    % parforProgress(0); % 清理文件并显示总进度
    
    narginchk(0, 1);
    
    if nargin < 1
        N = -1;
    end
    
    percent = 0;
    w = 20; % 进度条的宽度
    
    if N > 0
        
        % 检查并行池是否已打开，如果未打开则自动启动
        pool = gcp('nocreate'); % 检查当前并行池
        if isempty(pool)
            disp('并行池未打开，正在启动...');
            parpool; % 启动并行池
        end

        % 初始化：创建进度文件并覆盖写入任务总数 N
        f = fopen('parforProgress.txt', 'w');
        if f < 0
            error('当前目录 %s 无写入权限', pwd);
        end
    
        % 获取初始化时间（datetime 格式）
        startTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'); 
    
        % 写入开始时间和任务总数
        fprintf(f, '%s\n', char(startTime)); % 将 datetime 转为字符串
        fprintf(f, '%d\n', N);
        fclose(f);
        
        % 显示初始化的进度条
        if nargout == 0
            digits = floor(log10(N)) + 1;
            formattedStr = sprintf('%*d/%d', digits, 0, N);
            disp(['  0.0%[░', repmat('░', 1, w), ']   已完成任务: ', formattedStr, '   已运行时间: 00:00:00   预计剩余时间: --:--:--']);
        end
    
    elseif N == 0
        % 清理：删除进度文件并显示完成状态
        f = fopen('parforProgress.txt', 'r');
        fileStartTimeStr = fgetl(f); % 读取文件中的开始时间
        totalTasks = fscanf(f, '%d', 1); % 读取任务总数
        fclose(f);
        
        % 计算最终运行时间
        fileStartTime = datetime(fileStartTimeStr, 'Format', 'yyyy-MM-dd HH:mm:ss.SSS'); 
        currentTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'); 
        elapsedTime = currentTime - fileStartTime; % 计算总运行时间
        
        delete('parforProgress.txt'); % 删除进度文件
        percent = 100;
        
        % 显示完整的进度条并重新计算运行时间
        if nargout == 0
            formattedStr = sprintf('%d/%d', totalTasks, totalTasks);
            disp([repmat(char(8), 1, (w + 58 + length(formattedStr))), newline, '100.0%[', ...
                      repmat('█', 1, w + 1), ']   已完成任务: ', formattedStr, '   总运行时间: ', char(elapsedTime)]);
        end     
    else
        % 更新：检查进度文件是否存在
        if ~exist('parforProgress.txt', 'file')
            error('未找到 parforProgress.txt，请先运行 parforProgress(N) 进行初始化。');
        end
        
        % 记录当前任务完成一次
        f = fopen('parforProgress.txt', 'a');
        fprintf(f, '1\n');
        fclose(f);
        
        % 读取文件，计算已完成任务数和进度百分比
        f = fopen('parforProgress.txt', 'r');
        fileStartTimeStr = fgetl(f);
        totalTasks = fscanf(f, '%d', 1); % 读取任务总数
        digits = floor(log10(totalTasks)) + 1; % 读取其位数
        progress = fscanf(f, '%d'); % 读取已完成任务数
        fclose(f);
        completedTasks = length(progress);
        percent = completedTasks / totalTasks * 100;
    
        % 计算已运行时间
        currentTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'); 
        fileStartTime = datetime(fileStartTimeStr, 'Format', 'yyyy-MM-dd HH:mm:ss.SSS'); 
        elapsedTime = currentTime - fileStartTime; 
        
        % 计算预计剩余时间
        averageTimePerTask = elapsedTime / max(completedTasks, 1);
        remainingTasks = totalTasks - completedTasks;
        estimatedRemainingTime = averageTimePerTask * remainingTasks;
    
        % 更新显示进度条
        if nargout == 0
            perc = sprintf('%5.1f%%', percent); % 百分比格式化为宽度 5 的字符串，带 1 位小数
            formattedStr = sprintf(['%', num2str(digits), 'd/%d'], completedTasks, totalTasks); % 已完成任务数格式化为动态字符串
            numCompleted = round(percent * w / 100); % 已完成的进度条长度
            disp([repmat(char(8), 1, (w + 58 + length(formattedStr))), newline, perc, '[', ...
                  repmat('█', 1, numCompleted), repmat('░', 1, w + 1 - numCompleted), ...
                  ']   已完成任务: ', formattedStr, '   已运行时间: ', char(elapsedTime), '   预计剩余时间: ', char(estimatedRemainingTime)]);
    
        end
    end
end
