% pltspec_AmbiSeis()
%   plot spectrum for stacked AmbiSeis struct
%
% Usage
%   pltspec_AmbiSeis(AmbiSeis) % plot on new figure
%   [fspec, f] = pltspec_AmbiSeis(AmbiSeis, []) % skip plot
%   [fspec, f] = pltspec_AmbiSeis(AmbiSeis, 1, fmin, fmax,xscale,db) % plot on specific figure handle 1
%
% INPUT:
%   AmbiSeis, struct
%   figure_handle, fix figure num or use empty [] to skip plot
%   fmin, interested frequency range minF
%   fmax, interested frequency range maxF
%   xscale, linear or log x-axis
%   db, return DB amplitude or ABS amplitude, default DB
%
% OUTPUT:
%   f/fspec, spectrum amplitude
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 23-Apr-2020
%   add option foutFlag to support spectrum from preProcflow, 10-Dec-2020
%
% SEE ALSO:
%   pltspec
%
% ------------------------------------------------------------------
%%
function [fspec, f] = pltspec_AmbiSeis(AmbiSeis)
%
dt = AmbiSeis.dt;
npts = AmbiSeis.npts;
ntrace = AmbiSeis.ntrace;
% 
foutFlag = 0;
% add option to support spectrum from preProcflow
if isfield(AmbiSeis, 'procPar')
    if isfield(AmbiSeis.procPar, 'foutFlag') && AmbiSeis.procPar.foutFlag
        foutFlag = 1;
    end
end
% 
if foutFlag
    f = AmbiSeis.f;
    nfft = AmbiSeis.nfft;
    nf = length(f);
    fspec = zeros(nf, ntrace);
    for i = 1:ntrace
        fdata = AmbiSeis.Trace{i};
        %
        fspec(:,i) = sum(abs(fdata),2);
    end
else
    t = (0:npts-1)*dt;
    nf = ceil(npts/2)*2;
    fspec = zeros(floor(nf/2+1), ntrace);
    for i = 1:ntrace
        [fdata,f] = fftrl(AmbiSeis.Trace{i},t,0.1,nf);
        %
        fspec(:,i) = sum(abs(fdata),2);
    end
end
%

end

