% phaseshiftdsp2fk
% 	kernel codes for phase-shift method for MASW based dispersion analysis
% 	scan multiple trace seismic data along specific frequency/velocity direction
%   Reference on Park et al., 1998, 2006; Cheng et al., 2016
%	use angle to do azimuth adjustment for directional noise data
% 	use lrFlag to do reverse direction velocity scanning
% 	OUTPUT -> FK domain
% 
% Usage
% 	fk = phaseshiftdsp2fk(fdata,x,f,k)
%   fk = phaseshiftdsp2fk(fdata,x,f,k,angle,lrFlag)
%
% INPUT:
%   fdata, 2D seismic data spectrum [nf, ntrace]
% 	f/k, scanning vector along frequency and wavenumber [nf]/[nk]
%   x, offset info [ntrace]
%   angle, azimuthal adjustment degree [0~180], default 0
%   lrFlag
%       lrFlag = 0, positive direction and negative direction
%       lrFlag = 1, positive direction, default 1
%       lrFlag =-1, negative direction
%   normFlag, frequency normalization 1/ 0 or not
%
% OUTPUT:
%   fk, 2D dispersion energy matrix [nk,nf]
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 29-Mar-2020
% 	add normalization option, 04-Apr-2020
% 
% SEE ALSO:
%   FPhaseshift, phaseshiftdsp
% ------------------------------------------------------------------
%%
function fk = phaseshiftdsp2fk(fdata,x,f,k,angle,lrFlag,normFlag)

% default do not apply azimuth adjustment
if ~exist('angle','var') || isempty(angle)
	angle = 0;
end
% default choose forward/right-going direction
if ~exist('lrFlag','var') || isempty(lrFlag)
	lrFlag = 1;
end
% 
fdata = fdata./abs(fdata);
% 
nf = length(f);
nk = length(k);
%
% f=col2row(f,1);
x=col2row(x,2);
% 
fk = zeros(nf,nk);
tempfx = ones(nf,1)*x;
for i = 1:nk
    exptemp = exp(1i*2*pi*tempfx*k(i)*abs(cos(angle/180*pi)));
    if lrFlag == 1 || lrFlag == 0
        fk(:,i)=abs(sum(exptemp.*fdata,2));
    end
    if lrFlag == -1 || lrFlag == 0
        fk(:,i)=fk(:,i)+abs(sum(conj(exptemp).*fdata,2));
    end
end
fk = fk.';

%%------------------------ Spectral Normalization
if exist('normFlag','var') && normFlag
    fk=bsxfun(@rdivide, fk, max(abs(fk),[],1));
    fk=fk.^2;
end

fk(isnan(fk)) = 0;

end
