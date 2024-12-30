% FPhaseshift2fk
%   Calculate the dispersion image based on phase-shift method
%   Reference on Park et al., 1998
%   ==> OUTPUT in FK domain
%
% Usage
%   [fk,f,v]=FPhaseshift2fk(uxt,x,t,normFlag,fmin,fmax)
%   [fk,f,v]=FPhaseshift2fk(uxt,x,t,normFlag,fmin,fmax,figure_handle,cutFlag,picFilename)
%
% INPUT:
%   uxt, 2D seismic matrix [npts,ntrace]
%   x, 1D offset info [ntrace]
%   t, 1D time series [npts]
%   normFlag, frequency normalization 1/ 0 or not
%   fmin, interested frequency range minF
%   fmax, interested frequency range maxF
%   figure_handle, optional flag for imaging 1/0 or not
%   cutFlag, optional flag for cutoff Frequency cal 1/0 or not
%   picFilename, option filename for dispersion image
%
% OUTPUT:
%   fk, 2D dispersion energy matrix [nk,nf]
%   f, 1D frequency series [nf]
%   v, 1D velocity series [nk]
%
% DEPENDENCES:
%   1. fftrl, between, col2row, mwindow
%   2. cutFreq
%   3. pltDSPIMG
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 29-Mar-2020
%   remove dead traces, 09-Aug-2021
% ------------------------------------------------------------------
%%
function [fk,f,k]=FPhaseshift2fk2(uxt,x,t,normFlag,fmin,fmax)
%% 
% remove dead traces
mtrace = mean(uxt, 1);
uxt = uxt(:, ~isnan(mtrace));
x = x(~isnan(mtrace));
%%------------------------ initial parameters
% dx = mean(diff(unique(x)));
kmin = 0;
kmax = 0.1;
nk = 500;
k = linspace(kmin, kmax, nk);
nf = 600;
f = linspace(fmin, fmax, nf);
df = mean(diff(f));
dt = mean(diff(t));
nf = ceil(1/dt/df/2)*2;

%%------------------------ FFT
% 
[fdata,f] = fftrl(uxt,t,0.1,nf);

% 
fdata = fdata./abs(fdata);
% 
indexf = between(fmin,fmax,f,2);
f = f(indexf);
fdata = fdata(indexf,:);
% 
%%------------------------ Phase Shift
fk = phaseshiftdsp2fk(fdata,x,f,k);

%%------------------------ Spectral Normalization
if normFlag ==1
    fk=bsxfun(@rdivide, fk, max(abs(fk),[],1));
    fk=fk.^2;
end

fk(isnan(fk)) = 0;
