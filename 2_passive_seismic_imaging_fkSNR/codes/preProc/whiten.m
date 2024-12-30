% whiten()
%   spectral normalization for noise data
%   NOTE: change hw to check different smooth factor performance
%
% Usage
%   normSeis = whiten(dataSeis) % use abs
%   normSeis = whiten(dataSeis, 0) % use abs
%   normSeis = whiten(dataSeis, 1, 1) % use runsm with default hw 0.1%
%   normSeis = whiten(dataSeis, 10, 1) % use runsm with hw = 10 frequency points
%   normSeis = whiten(normSeis, 10, 1, 1) % output frequency domain wavefield
%
% INPUT:
%   dataSeis, [npts,numStack,ntrace] separated time-domain noise data
%       the first dim should be averaged, dataSeis could be multiple dim
%   smFlag, option for running smooth weighted
%   pltFlag, plot 1 or not 0
%   foutFlag, output frequency domain wavefield
%
% OUTPUT:
%   normSeis, normalized noise data
%   nfft, fft numbers for frequency domain output
%
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 25-Jul-2018
%   replace fft with fftrl to save half calculation, 20-Jan-2020
%   add option for smFlag to act as hw to define despike resolution,
%       smaller smFlag/hw indicates stricter whiten, 24-Apr-2020
%   add option for frequency domain wavefield output, 05-Jul-2020
%   add hugeDataFlag to control FFT sampling to avoid too high calculation burden, 01-Aug-2020
%
% SEE ALSO:
%   preProcflow
%
% ------------------------------------------------------------------
%%
function [normSeis, nfft]= whiten(dataSeis, smFlag, pltFlag, foutFlag, hugeDataFlag)

% dataSeis = data;
%  ----------------------------use size & reshape to adapt for multiple dim
sx = size(dataSeis); % [npts,numStack,ntrace]
len = cumprod(sx); len = len(end);
sx1 = sx(1);
sx2 = len/sx(1);
dataSeis = reshape(dataSeis,sx1,sx2);
%  ----------------------------apply fft
% avoid FFT further increase calculation burden
if exist('hugeDataFlag','var') && hugeDataFlag
    nfft = ceil(sx1/2)*2;
else
    nfft = max(2^nextpow2(sx1), 1024);
end
%%
dt = 1; t = (0:sx1-1)*dt; % dt has no meaning here
[dataSeisF, f] = fftrl(dataSeis, t, 0, nfft);
am = abs(dataSeisF);
%% apply running smooth with 1% band to cal whiten weight
if ~exist('smFlag','var') || smFlag == 0
    lw = am;
else
    if smFlag > 1
        hw = smFlag;
    else
        hw = max(ceil(nfft*0.005/2),2);
    end
    %
    lw = runSmooth(am,2*hw);
end
%% avoid lw to be zero
%
[indx, indy] = find(lw == 0);
if ~isempty(indx) && ~isempty(indy)
    whiteNoise = 2;
    lw_eps = whiteNoise/100 .* mean (lw,1);
    lw(indx, indy) = lw(indx, indy) + ones(length(indx),1)*lw_eps(indy);
end
%
normSeisF = dataSeisF ./ lw;
%% apply ifft
if exist('foutFlag','var') && foutFlag
    normSeis = normSeisF;
    sx(1) = length(f);
else
    normSeis = real(ifftrl(normSeisF, f));
    normSeis = normSeis(1:sx1,:);
end
%%
if exist('pltFlag','var') && pltFlag
    figure(3);clf;
    set(gcf, 'Units', 'centimeters', 'Position', [10, 10, 25, 20], 'Color', 'w');
    subplot(2,1,1)
    h1 = plot(f, norm2d(mean(am(:,1),2)),'k-');
    hold on
    h2 = plot(f,norm2d( mean(lw(:,1),2) ),'b-.');
    h3 = plot(f, norm2d(mean(abs(normSeisF(:,1)),2)),'r');
    hL = legend([h1 h2 h3],'raw amp','runmean amp','whiten amp');
    % set(hL,'Box','off');
    set(hL,'Color','w','EdgeColor','none');
    xlabel('Frequency sampling num')
    ylabel('Normlaized Amp')
    % xlim([1 nfft/2])
    box off
    setplt
    if ~(exist('foutFlag','var') && foutFlag)
        subplot(2,1,2)
        t = 1:sx1;
        h1 = plot(t, norm2d(dataSeis(:,1)),'k');
        hold on
        h2 = plot(t, norm2d(normSeis(:,1)),'r');
        hL = legend([h1 h2],'raw','whiten');
        % set(hL,'Box','off');
        set(hL,'Color','w','EdgeColor','none');
        xlabel('Time sampling num')
        ylabel('Normlaized Amp')
        box off
        setplt
    end
    saveimg(3,'whiten.pdf')
end
%%  ----------------------------reshape back to the original dim
normSeis = reshape(normSeis, sx);
end
