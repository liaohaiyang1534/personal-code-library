% fkfanfilter()
%   apply fk filter based on velocity fan
%   velocity must be in same direction! or move to fkpolyfilter function
%
% Usage
%   [dataout]=fkfanfilter(datain,dt,dx,300, 500)
%   [dataout, fkspec, k, f, filterin]=fkfanfilter(datain,dt,dx,-300,-500,1) 1/1000 taper reject
%   [dataout, fkspec, k, f, filterin]=fkfanfilter(datain,dt,dx,-300,-500,1,2) 2/1000 taper reject
%   [dataout, fkspec, k, f, filterin]=fkfanfilter(datain,dt,dx,-300,-500,1,2, 4, 4) 2/1000 taper reject
%
% INPUT:
%   datain, input x-t data matrix
% 	dt/dx, time/spacial interval
% 	vmin/vmax, velocity fan boundary 
% 	rejectFlag, band reject 1 or band pass 0, default 0
% 	taperPercent, tapering percent for the bounder, default 1 [1 unit 1/1000]
%   timesNT/timesNX, times for dense time/spatial directions which would
%       help improve the filter performance
%
% OUTPUT:
%   dataout, fk filtered x-t data matrix
% 	k/f/fkspec, filter spectrum
% 	filterin, filter zone in fk domain
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 06-Mar-2019
%   add sysFlag to fulfill sys fan filter, 21-Apr-2020
%   replace inpolygon with inpoly2 for speedup, 31-May-2020
%   fix no-tapper bug by converting logical outputs from inpoly2 into
%   double, 20-Sep-2020
%
% SEE ALSO:
%   fkpolyfilter
% ------------------------------------------------------------------
%
function [dataout, fkspec, k, f, filterin, poly, matfilt] = fkfanfilter(datain,dt,dx,vmin,vmax,rejectFlag,taperPercent,timesNT,timesNX,sysFlag)
%%
if ~exist('rejectFlag', 'var')
    rejectFlag = 0;
end
%
if ~exist('taperPercent', 'var')
    taperPercent = 1;
end
taperPercent = taperPercent/1000;

%----------define k/f axis-------------
[npts,ntrace]=size(datain);
%
npts2 = npts;
ntrace2 = ntrace;
% dense time/frequency domain
if exist('timesNT','var') && ~isempty(timesNT)
    npts2 = npts2*timesNT;
end
% dense spatial/wavenumber domain
if exist('timesNX','var') && ~isempty(timesNX)
    ntrace2 = ntrace2*timesNX;
end
%
npts2=2^nextpow2(npts2);
ntrace2=2^nextpow2(ntrace2);

if rejectFlag==0
    matfilt=zeros(npts2,ntrace2); %initializing filter matrix
elseif rejectFlag==1
    matfilt=ones(npts2,ntrace2); %initializing filter matrix
end

kmax=1/(2*dx); %Nyquist wavenumber
fmax=1/(2*dt); %Nyquist frequency
k = -kmax+kmax*2/ntrace2 : kmax*2/ntrace2 : kmax;
f = 0 : 2*fmax/npts2 : fmax;
[xmat,ymat]=meshgrid(k,f); %creating polymatrix

%%
%-------------computing fft---------------
fkdata=fftshift(fft2(datain,npts2,ntrace2));
% flip k axis to keep uniform with the positive direction from L to R
fkdata=fliplr( fkdata );
%%
% %-------------define polygon for fan---------------
k_bound = sign(vmax)*kmax;
poly = zeros(4,2);
poly(2:3,1) = k_bound;
poly(2, 2) = k_bound*vmin;
poly(3, 2) = k_bound*vmax;
%
if exist('sysFlag','var') && sysFlag
    poly2 = zeros(7,2);
    poly2(1:4, :) = poly;
    poly2(5:6, 1) = poly(2:3, 1)*-1;
    poly2(5:6, 2) = poly(2:3, 2);
    poly = poly2;
end
%%
%--------finding points in polygon---------
% filterin=inpolygon(xmat,ymat,poly(:,1),poly(:,2));
% inpoly2 is 20 more times faster than inpolygon
[stat] = inpoly2([xmat(:),ymat(:)],poly) ;
[nf, nk] = size(xmat);
filterin = double(reshape(stat, nf, nk));

%-------------mean filtering / taper---------------
nfreq=length(f);  % nfreq = npts2/2 + 1
%
taperNr = max(round(taperPercent*ntrace2), 5);
%
taperNc = max(round(taperPercent*nfreq), 5);
%
filterin = smooth2a(filterin, taperNr, taperNc);
% figure(5);clf
% imagesc(k,f,filterin)
% axis xy
% hold on
% plot(k, k*vmin,'r-.','LineWidth',2)
% plot(k, k*vmax,'r-.','LineWidth',2)
%%
%---------inverting filter matrix----------
if rejectFlag==1
    filterin=1-filterin;
end

%---------creating filter matrix------------
matfilt(nfreq:-1:1,:)= fliplr(filterin);
matfilt(npts2-nfreq+1:npts2,:) = filterin;

%---------------filtering--------------------
fd=fkdata.*matfilt;
%
fkspec = fd(npts2-nfreq+1:npts2, :) ;
%---------computing inverse fft--------------
fd = fliplr( fd );
%
dataout=ifft2(fftshift(fd));
dataout=real(dataout(1:npts,1:ntrace));

