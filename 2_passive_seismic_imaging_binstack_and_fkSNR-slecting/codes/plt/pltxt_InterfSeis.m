% pltxt_InterfSeis()
%   plot one segment InterfSeis struct
%
% Usage
%   pltxt_InterfSeis(InterfSeis, numIndex) % plot on new figure
%   [uxt, x, t] = pltxt_InterfSeis(InterfSeis, numIndex,figure_handle,normFlag,wiggleFlag)
%
% INPUT:
%   InterfSeis, struct
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
function [uxt, x, t] = pltxt_InterfSeis(InterfSeis, numIndex,figure_handle,normFlag,wiggleFlag)
%%
if ~exist('numIndex','var') || isempty(numIndex)
    numIndex = InterfSeis.numStack;
end
% 
if strcmp(InterfSeis.tfpresent,'temporal')
	%
	t = InterfSeis.tAxes;
	x = InterfSeis.Offset;
% 	uxt = InterfSeis.Shot{numIndex};
	uxt = InterfSeis.StackShot{numIndex};
	% 
else
	error('pltxt_InterfSeis only works for temporal/spectral InterfSeis struct!')
end
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

