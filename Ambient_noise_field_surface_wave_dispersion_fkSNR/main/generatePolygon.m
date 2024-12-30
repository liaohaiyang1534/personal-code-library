function polyData = generatePolygon(points, numPoints)
    % 生成多边形数据的函数
    % 输入:
    %   points : 一个 Nx2 矩阵，第一列为 x 坐标，第二列为 y 坐标
    %   numPoints : 最终生成的插值点数量
    % 输出:
    %   polyData : 一个 numPoints x 2 矩阵，包含插值后的 x 和 y 坐标

    % 检查输入的有效性
    if size(points, 2) ~= 2
        error('输入必须是一个 Nx2 矩阵。');
    end

    % 计算点的凸包
    K = convhull(points(:, 1), points(:, 2)); % 获取凸包的点的索引
    hullPoints = points(K, :); % 获取凸包的坐标点
    x = hullPoints(:, 1);
    y = hullPoints(:, 2);
    
    % 关闭多边形：确保第一个点与最后一个点相连
    if ~isequal(hullPoints(1, :), hullPoints(end, :))
        hullPoints = [hullPoints; hullPoints(1, :)];
        x = hullPoints(:, 1);
        y = hullPoints(:, 2);
    end

    % 计算每条边的长度
    segmentsX = diff(x);
    segmentsY = diff(y);
    segmentsLength = sqrt(segmentsX .^ 2 + segmentsY .^ 2);
    
    % 计算总长度并保证有边
    totalLength = sum(segmentsLength);
    if totalLength == 0
        error('所有输入点无法形成有效多边形。');
    end

    % 计算每条边上的插值点
    pointsPerSegment = round((segmentsLength / totalLength) * numPoints);
    pointsPerSegment = pointsPerSegment(pointsPerSegment > 0); % 移除无效的零值

    % 初始化插值的 x 和 y 容器
    interpolatedX = [];
    interpolatedY = [];

    % 在每条边上进行插值
    for i = 1:length(hullPoints)-1
        % 确保不超出数组边界
        numPointsPerSegment = pointsPerSegment(min(i, end));
        xi = linspace(x(i), x(i+1), numPointsPerSegment + 1); % 生成点
        yi = linspace(y(i), y(i+1), numPointsPerSegment + 1); % 生成点
        interpolatedX = [interpolatedX, xi(1:end-1)]; % 避免重复
        interpolatedY = [interpolatedY, yi(1:end-1)]; % 避免重复
    end

    % 确保最终插值数量为numPoints
    if length(interpolatedX) > numPoints
        interpolatedX = interpolatedX(1:numPoints);
        interpolatedY = interpolatedY(1:numPoints);
    elseif length(interpolatedX) < numPoints
        % 如果不足，均匀插值
        interpolatedX = linspace(min(interpolatedX), max(interpolatedX), numPoints);
        interpolatedY = linspace(min(interpolatedY), max(interpolatedY), numPoints);
    end

    % 形成最终的矩阵
    polyData = [interpolatedX', interpolatedY']; % 将 x 和 y 合并为矩阵
end