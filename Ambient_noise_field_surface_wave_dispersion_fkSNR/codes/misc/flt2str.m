function s = flt2str(a,pre)
% flt2str()
%   convert float variable to string variable and keep pre
%
% Usage
%   s = flt2str(a,pre)
%
% INPUT:
%   a, float variables [1x1]
%   pre, precision to be keep, default 2 like 2.00
%
% OUTPUT:
%   s, string various with format precision 
%   
% DEPENDENCES:
%
% AUTHOR:
%   F. CHENG ON mars-OSX.local
%
% UPDATE HISTORY:
%   Initial code, 12-Oct-2017
%
% SEE ALSO:
%   flt2str2
% ------------------------------------------------------------------
if nargin < 2
    pre = 2;
end
temp = num2str(a);
index = find(temp=='.');
if isempty(index)
    index = length(temp)+1;
    temp=[temp,'.'];
end
if index+pre < length(temp)
    s = temp(1:index+pre);
else
    s = temp;
    for i=1:index+pre-length(temp) 
        s = [s,'0'];
    end
end