function uxt=norm2d(uxt,ndim,norm_type)
% norm2d
%   normalize 2D matrix along row/1 or column/2 direction
%   as for XT-domain (uxt(npts,ntrace)), n=1
%   as for FV-domain (fv(nv,nf)), n=1
%
% Usage
%   [uxt]=norm2d(uxt,n)
%
% INPUT:
%   uxt, 2D seismic matrix [npts,ntrace]/[nv,nf]
%   ndim, optional flag to decide normalization direction 1/row or 2/column
%
% OUTPUT:
%   uxt, 2D XT matrix after normalization along n-direction
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 01-Dec-2017
%   add nan remove, 02-Mar-2019
% 	add norm norm_type to support 2-norm, 23-Feb-2021
% 	add rms and std normalization, 14-Oct-2021
%
% ------------------------------------------------------------------
%%
if ~exist('ndim','var')
    ndim=1;
end
%
if ~exist('norm_type','var')
    norm_type = 'abs';
end
% Normalization in the row/1 or column/2
switch norm_type
    case 'abs'
        uxt = bsxfun(@rdivide, uxt, max(abs(uxt),[],ndim));
    case '2norm'
        uxt = bsxfun(@rdivide, uxt, vecnorm(uxt, 2, ndim));
    case 'rms'
        if ndim==1
            uxt = bsxfun(@rdivide, uxt, ones(size(uxt,1),1)*rms(uxt, 1));
        else
            uxt = bsxfun(@rdivide, uxt, rms(uxt, 2)*ones(1,size(uxt,2)));
        end
    case 'std'
        if ndim==1
            uxt = bsxfun(@rdivide, uxt - ones(size(uxt,1),1)*mean(uxt,1), ones(size(uxt,1),1)*std(uxt,1,1));
        else
            uxt = bsxfun(@rdivide, uxt - mean(uxt,2)*ones(1,size(uxt,2)), std(uxt,1,2)*ones(1,size(uxt,2)));
        end
end
%
% uxt(isnan(uxt)) = 0;

