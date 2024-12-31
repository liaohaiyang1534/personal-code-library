% pltxt_AmbiSeis()
%   combine AmbiSeis matrix and plot one segment AmbiSeis struct
%
% Usage
%   pltxt_AmbiSeis(AmbiSeis, numIndex) % plot on new figure
%   [uxt, x, t] = pltxt_AmbiSeis(AmbiSeis,0) % combine ambiseis matrix without considering overlap
%   [uxt, x, t] = pltxt_AmbiSeis(AmbiSeis, numIndex,figure_handle,normFlag,wiggleFlag)
%
% INPUT:
%   AmbiSeis, struct
%   numIndex, index for segment
%   normFlag, optional flag for frequency normalization 1/ 0 or not
%   figure_handle, optional flag for new figure numeric or [] to hold on the current figure
%   wiggleFlag, optional for wiggle plot or image plot, default 0
%
% OUTPUT:
%   uxt, x, t, shot gather for specific index segment
%
% DEPENDENCES:
%   pltseis
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 23-Apr-2020
%
% SEE ALSO:
%   pltxt_InterfSeis
%
% ------------------------------------------------------------------
%%
function [uxt, x, t] = pltxt_AmbiSeis(AmbiSeis, numIndex,figure_handle,normFlag,wiggleFlag)
%
dt = AmbiSeis.dt;
npts = AmbiSeis.npts;
ntrace = AmbiSeis.ntrace;
x = zeros(ntrace, 1);
if ~exist('numIndex','var') || strcmp(numIndex,'all')
    numIndex = 1:AmbiSeis.numStack;
end
%
uxt = zeros(npts*length(numIndex), ntrace);
for i = 1:ntrace
    E = reshape(AmbiSeis.Trace{i}(:,numIndex), 1, []);
    uxt(:,i) = E;
    x1=AmbiSeis.Geometry(1,1); y1=AmbiSeis.Geometry(1,2);
    x2=AmbiSeis.Geometry(i,1); y2=AmbiSeis.Geometry(i,2);
    x(i) = sqrt((x1-x2).^2 + (y1-y2).^2);
end
% 
npts = size(uxt,1);
t = (0:npts-1)*dt;
%
if exist('figure_handle','var') && figure_handle == 0
    return;
end
%
if ~exist('figure_handle','var')
    figure_handle = [];
end
%
if ~exist('normFlag','var')
    normFlag = 1;
end
%
if ~exist('wiggleFlag','var')
    wiggleFlag = 1;
end
%
pltseis(x,t,uxt,normFlag,figure_handle,wiggleFlag)

end

