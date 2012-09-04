function [k, n] = RRD(d, Rd)
% Rosin-Rammler Diagram plot and parameter estimation function.
% Parameters are estimated using non-linear fitting routine. 
%
% Following equation is used:
%
% R(d) = 100*exp(-1*((d/k)^n))
%
% where:
% d - mesh sizes
% Rd - percent material retained (cumulative)
% k - size parameter
% n - uniformity parameter
%
% Example:
% d = [0.08 0.50 1.25 2 4 6.3 8 12.5 16 40]
% Rd = [95.61 87.71 82.45 79.78 73.28 66.98 63.21 55.4 49.91 23.95]
% 
% [k, n] = RRD(d, Rd)
%
% >> k = 27.0236
% >> n = 0.5946
%
% Ing. Ivan Brezani
% ivan.brezani@tuke.sk
%
% 2011-12-21

if isempty(d)==1
    error('Mesh size vector is empty. Enter some values.');
elseif isempty(Rd)==1
    error('Percent material retained vector is empty. Enter some values.');
elseif length(d) ~= length(Rd)
    error('Vectors are not equal length');
elseif d ~= sort(d)
    error('Mesh size vector must be monotonically increasing');
elseif Rd ~= sort(Rd, 'descend')
    error('Percent of material retained vector must be monotonically decreasing');
elseif sum(d <= 0) >= 1
    error('Mesh size of zero or negative values not permited');
elseif sum(Rd <= 0) >= 1
    error('Zero or negative values of percent material retained not permited');
elseif sum(Rd >= 100) >= 1
    error('100% material retained or higher values not permited');
elseif length(d) <= 3
    error('Not enoug values for parameter estimation');
end
    

fit = inline('100*exp(-1*((d./fit(1)).^fit(2)))','fit','d');
fit = lsqcurvefit(fit,[10 1],d,Rd);

k = fit(1);
n = fit(2);

Y(1) = fit(1)*((-1*log(0.999))^(1/fit(2)));
Y(2) = fit(1)*((-1*log(0.0001))^(1/fit(2)));

y = -1*log10(log10(100./Rd));
semilogx(d, y, 'ro', Y, -1*log10(log10(100./[99.9 0.01])), 'b-');

% Double logarithmic Y-axis
y = [];
y = [0.01 0.1 1 5 10 20 30 40 50 60 70 75 80 85 90 92 94 96 98 99 99.5 99.8 99.9];
y = -1*log10(log10(100./y));
set(gca,'ytick', y);
set(gca,'yticklabel',{' ', '0.1', '1','5','10','20','30','40','50','60','70', '75', '80','85','90','92','94','96','98','99','99.5','99.8',' '});
set(gca,'YDir','reverse');
set(gca,'YLim', [min(y) max(y)]);


% Graph labels
xlabel('Mesh size');
ylabel('Retained on screen [%]');
title('Rosin-Rammler Diagram');
grid on;


end

