Vrms = 230;
R = 9.5;
P = 1;
f = 50;
T = 0.015;

I = sqrt(((2*Vrms^2)/(R^2*P))*(T/2 - (1/(8*pi*f))*sin(4*pi*f*T)))
Q = I^2*R