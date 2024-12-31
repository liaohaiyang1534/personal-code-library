% pltseis
%   Plot seismic wiggle/Image on new or existing figure/subfigure
%
% Usage
%   pltseis(x,t,uxt)
%   pltseis(x,t,uxt,normFlag,[],wiggleFlag)
%   pltseis(x,t,uxt,normFlag,figure_handle,wiggleFlag)
%
% INPUT:
%   uxt/x/t, seismic matrix/axes
%   normFlag, optional flag for frequency normalization 1/ 0 or not
%   figure_handle, optional flag for new figure numeric or [] to hold on the current figure
%   wiggleFlag, optional for wiggle plot or image plot, default 0
%
% OUTPUT:
%
% DEPENDENCES:
%   1. deSample2d
%   2. Figure
%   3. rwb
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 22-Nov-2016
%   add wiggle option to switch different mode, 29-Mar-2020
% ------------------------------------------------------------------
%%
function pltseis(x,t,uxt,normFlag,figure_handle,wiggleFlag)
%
if exist('figure_handle', 'var') && ~isempty(figure_handle)
    figure(figure_handle);clf
    set(gcf,'Units','centimeters','Position',[2 2 10 10]);
end
%
if ~exist('wiggleFlag', 'var') || isempty(wiggleFlag)
    wiggleFlag = 0;
end
%
if size(uxt, 2) < 10
    wiggleFlag = 1;
end
% 
if exist('normFlag', 'var') && normFlag
    uxt = bsxfun(@rdivide, uxt, max(abs(uxt),[],1));
end
if wiggleFlag
    wigb(uxt,x,t,'k');
    box on
    set(gca,'XAxisLocation','bottom');
else
    h = imagesc(x,t,uxt);
    set(h,'CDataMapping','scaled')
    set(h,'alphadata',~isnan(uxt))
    colormap(gca, jet)
end
axis ij
xlabel('Offset (m)');
ylabel('Time (sec)');

end


