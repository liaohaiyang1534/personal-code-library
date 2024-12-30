function [uxt_stack, x_stack, t, uxt, x] = mkvsg_InterfSeis(InterfSeis,figure_handle)
% extract virtual-source gather matrix from InterfSeis struct
% 
% F. Cheng, Jul-16-2023
% 
if ~exist("figure_handle",'var')
    figure_handle = 10;
end
% 
[uxt, x, t] = pltxt_InterfSeis(InterfSeis, [],figure_handle,1,0);
%
iprocPar = InterfSeis.procPar;
% 
if strcmp( iprocPar.vsIndex, 'cn2' )
    %
    [uxt_stack, x_stack] = copstacking(uxt,x);

else
    uxt_stack = uxt;
    x_stack = x;
end

end