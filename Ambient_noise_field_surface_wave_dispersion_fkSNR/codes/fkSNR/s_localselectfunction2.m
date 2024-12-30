function interf_matrix = s_localselectfunction2(interf_matrix, i, procPar)
% 
% custom data-selection local function 
% paramters will be passed into function with procPar
% 
% Writting by F. Cheng, Jul-15-2023
% 
fkSNR = procPar.fkSNR;
lrSNR = procPar.lrSNR;
snrThreshold = procPar.snrThreshold;
%
if fkSNR(i) < snrThreshold
    interf_matrix = interf_matrix .* 0;
else
    if lrSNR(i) < 1
        interf_matrix = flipud( interf_matrix );
    end
end

