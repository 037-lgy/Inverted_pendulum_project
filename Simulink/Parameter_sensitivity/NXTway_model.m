function [A1,B1,A2,B2] = NXTway_model(p)

g = 9.81;

m = p.m;
R = p.R;
M = p.M;
W = p.W;
D = p.D;
H = p.H;
L = p.L;

Jw = m * R^2 / 2;

Jpsi = M * L^2 / 3;
Jphi = M * (W^2 + D^2) / 12;

fm = p.fm;
fw = p.fw;

Jm = p.Jm;
Rm = p.Rm;
Kb = p.Kb;
Kt = p.Kt;
n = p.n;

alpha = n * Kt / Rm;
beta = n * Kt * Kb / Rm + fm;

tmp = beta + fw;

E_11 = (2*m + M)*R^2 + 2*Jw + 2*n^2*Jm;
E_12 = M*L*R - 2*n^2*Jm;
E_22 = M*L^2 + Jpsi + 2*n^2*Jm;

detE = E_11*E_22 - E_12^2;

A1_32 = -g*M*L*E_12/detE;
A1_42 =  g*M*L*E_11/detE;

A1_33 = -2*(tmp*E_22 + beta*E_12)/detE;
A1_43 =  2*(tmp*E_12 + beta*E_11)/detE;

A1_34 = 2*beta*(E_22 + E_12)/detE;
A1_44 = -2*beta*(E_11 + E_12)/detE;

B1_3 = alpha*(E_22 + E_12)/detE;
B1_4 = -alpha*(E_11 + E_12)/detE;

A1 = [
    0 0 1 0
    0 0 0 1
    0 A1_32 A1_33 A1_34
    0 A1_42 A1_43 A1_44
];

B1 = [
    0 0
    0 0
    B1_3 B1_3
    B1_4 B1_4
];

I = m*W^2/2 + Jphi + (Jw + n^2*Jm)*W^2/(2*R^2);
J = tmp*W^2/(2*R^2);
K = alpha*W/(2*R);

A2 = [
    0 1
    0 -J/I
];

B2 = [
    0 0
    -K/I K/I
];

end