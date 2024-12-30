function forProgress(N)
    % for 循环中显示任务进度条工具
    %
    % 功能说明:
    % 1. 初始化任务进度:
    %    - 调用 'forProgress(N)' 创建任务总数为 N 的进度条。
    %    - 显示初始状态的任务进度条，进度为 0%。
    % 2. 动态更新任务进度:
    %    - 在 for 循环内，每次任务完成时调用 'forProgress()'。
    %    - 自动计算已完成任务的百分比、已运行时间和预计剩余时间。
    %    - 实时更新任务进度条，显示动态任务信息。
    % 3. 完成任务清理:
    %    - 调用 'forProgress(0)' 显示任务完成的最终状态。
    %    - 清理内部状态并覆盖旧的进度条显示。
    %
    % 使用示例:
    % % 假设任务总数为 N
    % forProgress(N); % 初始化任务进度
    % for i = 1:N
    %     pause(0.1); % 模拟任务耗时
    %     forProgress(); % 每次任务完成后更新进度
    % end
    % forProgress(0); % 清理并显示任务完成状态

    persistent totalTasks completedTasks startTime progressWidth

    progressWidth = 21; % 进度条宽度

    if nargin >= 1 && N > 0
        % 初始化任务
        totalTasks = N;
        completedTasks = 0;
        startTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss');
        
        % 显示初始进度条
        formattedStr = sprintf('%*d/%d', floor(log10(N)) + 1, 0, N);
        disp(['  0.0%[', repmat('░', 1, progressWidth), ']   已完成任务: ', formattedStr, '   已运行时间: 00:00:00   预计剩余时间: --:--:--']);

    elseif nargin == 1 && N == 0
        % 清理任务并显示完成状态
        elapsedTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss') - startTime;

        % 显示完整进度条
        formattedStr = sprintf('%d/%d', totalTasks, totalTasks);
        disp([repmat(char(8), 1, (progressWidth + 57 + length(formattedStr))), newline, '100.0%[', ...
              repmat('█', 1, progressWidth), ']   已完成任务: ', formattedStr, '   总运行时间: ', char(elapsedTime)]);

        % 清理状态
        clear totalTasks completedTasks startTime progressWidth;
    else
        % 更新任务进度
        if isempty(totalTasks)
            error('请先运行 forProgress(N) 初始化任务总数。');
        end

        % 更新完成任务数
        completedTasks = completedTasks + 1;

        % 计算进度百分比
        percent = completedTasks / totalTasks * 100;
        numCompleted = round(percent * progressWidth / 100);

        % 计算已运行时间和预计剩余时间
        elapsedTime = datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss') - startTime;
        averageTimePerTask = elapsedTime / max(completedTasks, 1);
        remainingTasks = totalTasks - completedTasks;
        estimatedRemainingTime = averageTimePerTask * remainingTasks;

        % 显示更新后的进度条
        perc = sprintf('%5.1f%%', percent); % 百分比格式化
        formattedStr = sprintf('%*d/%d', floor(log10(totalTasks)) + 1, completedTasks, totalTasks);
        disp([repmat(char(8), 1, (progressWidth + 57 + length(formattedStr))), newline, perc, '[', ...
              repmat('█', 1, numCompleted), repmat('░', 1, progressWidth - numCompleted), ...
              ']   已完成任务: ', formattedStr, '   已运行时间: ', char(elapsedTime), '   预计剩余时间: ', char(estimatedRemainingTime)]);
    end
end
