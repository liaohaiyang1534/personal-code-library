function uxt=norm1d(uxt, norm_type)
% norm1d
%   normalize 1D vector
% 
% Usage
%   [uxt]=norm1d(uxt)
% 
% INPUT:
%   uxt, 1D seismic series
% 
% OUTPUT:
%   uxt, 1D series after normalization
% 
% DEPENDENCES:
% 	norm2d
% 
% AUTHOR:
%   F. CHENG ON mars-OSX.local
% 
% UPDATE HISTORY:
%   Initial code, 23-Jan-2020
%
% ------------------------------------------------------------------
%%
uxt = uxt(:);
%
if ~exist('norm_type','var')
    norm_type = 'abs';
end
% 
uxt=norm2d(uxt,1,norm_type);