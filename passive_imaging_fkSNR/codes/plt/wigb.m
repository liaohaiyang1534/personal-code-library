function wigb(uxt,x,t,lineColor,style,faceColor,linestyle,linewidth,amx)
% wigb(uxt,x,t,lineColor,style,faceColor,linestyle,linewidth,amx)
%
% WIGB: Plot seismic data using wiggles,
%   2008,12,24
%
% USAGE:
%   WIGB(uxt,x,t)
%   WIGB(uxt,x,t,lineColor)
%   ....
%   WIGB(uxt,x,t,lineColor,style,faceColor,linestyle,linewidth,amx)
%
% INPUT
%        uxt:     seismic data
%        x:     x-axis (offset)
%        t:     vertical axis (time or depth)
%        lineColor:  linecolor
%        style:   figure style option
%               > 1, wiggle style, default
%               > 2, only positive events style
%        faceColor:   fillcolor
%        linestyle:   Linestyle
%        linewidth:   Linewidth
%               > 0.5 pt is defaulted
%        amx:   maximnum amplitude
%
%
% Author:
% 	Xingong Li, Dec. 1995
% Changes:
%   Dec34,2008: change zeors line fillcolor to black(old is white), F, Cheng
%   Nov4th,2015: Replace 'Erasemode' by ANIMATEDLINE function, F. Cheng
%	Jun11,1997: add amx
% 	May16,1997: updated for v5 - add 'zeros line' to background color
% 	May17,1996: if scal ==0, plot without scaling
% 	Aug06,1996: if max(tr)==0, plot a line
%
% Recent History: F. Cheng
%   Nov04,2015: check Matlab version and choose to use 'Erasemode' property
%       or ANIMATEDLINE function
%   	release < R2014a, Erasemode property will be used to plot traces lines
%   	release > R2014a, 'Erasemode' will be replaced by ANIMATEDLINE function
%   Mar13,2016: shut dead trace
%   Nov27,2016: add options for lines control
%   Jan01,2018: add quick imaging control
%   Apr18 2018: rewrite the line control
%
% wigb(data)

if nargin == 0, ntrace=10;npts=10; uxt = rand(npts,ntrace)-0.5; end
%
[npts,ntrace]=size(uxt);trmx= max(abs(uxt));

if (nargin <= 8); amx=mean(trmx);  end
if (nargin <= 7); linewidth = 0.5;  end
if (nargin <= 6); linestyle = '-';  end
if (nargin <= 5); faceColor='k';  end
if (nargin <= 4); style=1;  end
if (nargin <= 3); lineColor='k';  end
if (nargin <= 2); t=[1:npts]; end
if (nargin <= 1); x=[1:ntrace]; end

if ntrace <= 1
    error(' ERR:PlotWig: ntrace has to be more than 1');
end

% take the average as dx
dx1 = abs(x(2:ntrace)-x(1:ntrace-1));
dx = median(dx1);
dz=t(2)-t(1);
scal=1;
uxt = uxt * dx /amx;
uxt = uxt * scal;
% fprintf(' PlotWig: data range [%f, %f], plotted max %f \n',xmn,xmx,amx);

% set display range
x1=min(x)-1.0*dx; x2=max(x)+1.0*dx;
z1=min(t)-dz; z2=max(t)+dz;
% set figure properties
set(gca,'NextPlot','add','Box','on', ...
    'XLim', [x1 x2], ...
    'YDir','reverse', ...
    'YLim',[z1 z2],...
    'xAxisLocation','top');
t=t';   % input as row vector
zstart=t(1);
zend  =t(npts);
%-------- fill color
for i=ntrace:-1:1
    if trmx(i) ~= 0
        tr=uxt(:,i);  % --- one scale for all section
        s = sign(tr);
        i1= find( s(1:npts-1) ~= s(2:npts) ); % zero crossing points
        % consider of dead traces, who have no zero crossing points
        if isempty(i1)
            continue
        end
        zadd = i1 + tr(i1) ./ (tr(i1) - tr(i1+1)); %locations with 0 amplitudes
        aadd = zeros(size(zadd));
        [zpos] = find(tr >0);
        [zz,iz] = sort([zpos; zadd]);   % indices of zero point plus positives
        aa = [tr(zpos); aadd];
        aa = aa(iz);
        % be careful at the ends
        if tr(1)>0
            a0=0; z0=1.00;
        else
            a0=0; z0=zadd(1);
        end
        if tr(npts)>0
            a1=0; z1=npts;
        else
            a1=0; z1=max(zadd);
        end
        
        zz = [z0; zz; z1; z0];
        aa = [a0; aa; a1; a0];
        zzz = zstart + zz*dz -dz;
        if (style==1 || style==2 )
            % positive part fill color
            patch( aa+x(i) , zzz,  faceColor);
            % remove zero line
            line( 'Color',[1 1 1], ...
                'Xdata', x(i)+[0 0], 'Ydata',[zstart zend]);
        end
        % negative part line
        if (style==1 )
            line( 'Color',lineColor,'LineWidth',linewidth,'linestyle',linestyle, ...
                'Xdata',tr+x(i), 'Ydata',t);
        end
    else %ZEROS LINES
        line( 'Color',lineColor,'LineWidth',linewidth,'linestyle',linestyle, ...
            'Xdata',[x(i) x(i)], 'Ydata',[zstart zend])
    end
end

xlabel('Trace | Offset (m)');
ylabel('Time(sec)');
box off
% set(gca,'Fontsize',12,'FontWeight','normal');
% set(get(gca,'XLabel'),'FontWeight','Bold','FontSize',14,'Interpreter','latex')
% set(get(gca,'YLabel'),'FontWeight','Bold','FontSize',14,'Interpreter','latex')
% set(gca,'xminortick','on');
% set(gca,'yminortick','on');
% set(gca,'ticklength',[0.02 0.005]);
% set(gca,'tickdir','out');
grid on
end





