function [fkSNR,lrSNR,filterin,filterin1,filterin2] = s_calfkSNR(data,dt,dx,procPar)
%
% Test fkSNR on IVDF data demo
%
% F. Cheng, Jul-16-2023
%
% ------------------------ check process parameter
%
%%
[npts, ntrace] =size(data);
%
x = (1:ntrace)*dx;
t = (0:npts-1)*dt;
%
fmin        = procPar.fmin;
fmax        = procPar.fmax;
vmin        = procPar.vmin;
vmax        = procPar.vmax;
% define fk filter parameter
rejectFlag = 0; taperPercent =2; timesNT = 2; timesNX =2; sysFlag = 0;
% forward-going wavefield energy
uxt1 = fkfanfilter(data,dt,dx, max(vmin-40, 10),vmax+200,rejectFlag,taperPercent,timesNT,timesNX,sysFlag);
[fk_p,f,k] = FPhaseshift2fk2(uxt1,x,t,0,fmin,fmax);
% backward-going wavefield energy
uxt2 = fkfanfilter(fliplr(data),dt,dx, max(vmin-40, 10),vmax+200,rejectFlag,taperPercent,timesNT,timesNX,sysFlag);
[fk_n] = FPhaseshift2fk2(uxt2,x,t,0,fmin,fmax);
%
if isfield(procPar, 'filterin') && ~isempty(procPar.filterin) ...
        && ~isempty(procPar.filterin1) && ~isempty(procPar.filterin2)
    % filterin matrix could be pre-defined and passed to function from procPar struct
    filterin = procPar.filterin;    % primary surface wave window
    filterin1 = procPar.filterin1;  % signal fundamental window (filterin > filterin1)
    filterin2 = procPar.filterin2;  % noise fundamental window
else
    % or define filterin matrix using defined signal/noise fk windows (polys)
    % focus on fundamental lower-frequency part
    % poly, primary surface wave window
    % poly1, signal fundamental window (filterin > filterin1)
    % poly2, noise fundamental window
    %
    [xmat, ymat] = meshgrid(f,k);
    [stat] = inpoly2([xmat(:),ymat(:)],procPar.poly) ;  % poly could be a looser window
    [nk, nf] = size(xmat);
    filterin = double(reshape(stat, nk, nf));
    %
    [stat] = inpoly2([xmat(:),ymat(:)],procPar.poly1) ;
    filterin1 = double(reshape(stat, nk, nf));
    %
    [stat] = inpoly2([xmat(:),ymat(:)],procPar.poly2) ;
    filterin2 = double(reshape(stat, nk, nf));
end
% SNR of L/R shots
lrSNR = rms(fk_p(filterin>0)) / rms(fk_n(filterin>0));
%
if lrSNR > 1
    fk = wiener2(fk_p, 4, 4);
else
    fk = wiener2(fk_n, 4, 4);
end
%
fk = norm2d(fk);
% SNR of the target modes
fkSNR = rms(fk(filterin1>0)) ./ rms(fk(filterin2>0));
%
if isfield(procPar, 'fkSNRplt') && procPar.fkSNRplt
    figure(10);clf
    set(gcf,'Units','normalized','Position',[0.2 0.2 0.8 0.5]);
    subplot(1,2,1)
    imagesc(x,t,data)
    ylabel('Time (sec)');xlabel('Offset (m)')
    title('noise waveform segment')
    subplot(1,2,2)
    h = pltdsp(f,k,fk,0,[],x, 1);
    imgdata = filterin1;
    imgdata(filterin1<1) = 0.3;
    set(h,'alphadata',imgdata)
    hold on
    h1 = plot(procPar.poly(:,1), procPar.poly(:,2), 'k--','LineWidth',2);
    h2 = plot(procPar.poly1(:,1), procPar.poly1(:,2), 'g--','LineWidth',2);
    h3 = plot(procPar.poly2(:,1), procPar.poly2(:,2), 'b--','LineWidth',2);
    title(sprintf('fkSNR=%.2f w. lrSNR=%.2f', fkSNR, lrSNR))
    legend([h1 h2 h3], {'loose window for lr', ...
        'narrower window for single', 'loose windows for noise'},...
        'Location','southeast')
    %
end



end