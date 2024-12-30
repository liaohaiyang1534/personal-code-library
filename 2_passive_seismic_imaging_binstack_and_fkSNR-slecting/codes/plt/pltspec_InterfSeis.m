% pltspec_InterfSeis()
%   plot spectrum for stacked InterfSeis struct
%
% Usage
%   pltspec_InterfSeis(InterfSeis) % plot on new figure
%   [fspec, f] = pltspec_InterfSeis(InterfSeis, []) % skip plot
%   [fspec, f] = pltspec_InterfSeis(InterfSeis, 1, fmin, fmax,xscale,db) % plot on specific figure handle 1
%
% INPUT:
%   InterfSeis, struct
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
%
% SEE ALSO:
%   pltspec
%
% ------------------------------------------------------------------
%%
function [fspec, f] = pltspec_InterfSeis(InterfSeis)
%
if strcmp(InterfSeis.tfpresent,'temporal')
    t = InterfSeis.tAxes;
    uxt = InterfSeis.StackShotMatrix;
    nf = ceil(InterfSeis.npts/2)*2;
    [fdata,f] = fftrl(uxt,t,0.1,nf);
    %
    fspec = sum(abs(fdata),2);
else
    f = InterfSeis.tAxes;
    fspec = mean( abs(InterfSeis.StackShotMatrix), 2);
end

