% copstacking()
%   Common Offset Stacking for CN2 Interferometry shot gather
% 	In terms of dispersion imaging with virtual-source gather, we assume a 1-D velocity model below the cc gather
% 	common offset stacking is potential to improve data utilization and average spatial abnormality
%
% Usage
%   [uxt_stack, x_stack] = copstacking(uxt, x)
%   [uxt_stack, x_stack] = copstacking(uxt, x, bin)
%
% INPUT:
%   uxt, npts x CN2 virtual-source gather
% 	x, CN2 offset for each channel
% 	bin, new spatial interval for cop average
%
% OUTPUT:
%   uxt_stack, sorted/averaged one shot gather
% 	x_stack, sorted offset
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 16-Jan-2020
%   add offset sort function, 24-Apr-2023
%
% SEE ALSO:
%
% ------------------------------------------------------------------
%%
function [uxt_stack, x_stack, nanIndex] = copstacking(uxt, x, bin, rmnan)
%
[npts] = size(uxt,1);
if ~exist('bin', 'var')
    bin = mean(diff(unique(x)));
end
%
if ~exist('rmnan', 'var')
    rmnan = 1;
end
% x_stack = min(x):bin:max(x);
x_stack = (round(min(x)/bin):round(max(x)/bin))*bin;
ntrace_stack = length(x_stack);
uxt_stack = nan(npts, ntrace_stack);
nanIndex = [];
for i = 1:length(x_stack)
    index = between(x_stack(i)-bin/2, x_stack(i)+bin/2, x, 2);
    if ~isempty(index)
            uxt_stack(:, i) = mean(uxt(:, index), 2);
    else
        nanIndex = [nanIndex, i];
    end
end
%
if rmnan
    x_stack(nanIndex) = [];
    uxt_stack(:, nanIndex) = [];
end

