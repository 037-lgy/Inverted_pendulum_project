close all
clear all
clc

% Controller Parameters 
lego_selfbalance_plant
% Copyright 2011 The MathWorks, Inc.

% Servo Gain Calculation using Optimal Regulator
A_BAR = [A1, zeros(4, 1); C1(1, :), 0];
B_BAR = [B1; 0, 0];
 QQ = [
 	1, 0,   0, 0, 0
 	0, 6e5, 0, 0, 0
 	0, 0,   1, 0, 0
 	0, 0,   0, 1, 0
 	0, 0,   0, 0, 4e2
 	];
 RR = 1e3 * eye(2);

KK = lqr(A_BAR, B_BAR, QQ, RR);
% pre-calculated optimal gain matrix
%KK = [-0.8351  -34.1896   -1.2935   -2.8141   -0.4472
%     -0.8351  -34.1896   -1.2935   -2.8141   -0.4472];

  
k_f = KK(1, 1:4);					% feedback gain
k_i = KK(1, 5);						% integral gain
% suppress velocity gain because it fluctuates robot
k_f(3) = k_f(3) * 0.85;

% k_f = [-1.5, -209.7, -3.42, -9.34];
% lc = -1.5;
% Task Sample Rates
ts1 = 0.004;						% ts1 sample time [sec]
ts2 = 0.02;							% ts2 sample time [sec]
ts3 = 0.1;							% ts3 sample time [sec]

% Start Time of balancing and autonomous drive
time_start = 1250;                  % start time of balancing [msec] (= gyro calibration time)

% Parameters of Coulombic & Viscous Friction
pwm_gain = 1;						% pwm gain
pwm_offset = 0;						% pwm offset 

% Low Path Filter Coefficients
a_b = 0.8;							% average battery value
a_d = 0.8;							% suppress velocity noise
a_r = 0.996;						% smooth reference signal
a_gc = 0.8;							% calibrate gyro offset
% User Setting Values
k_thetadot = 0.3 / R;				% speed gain (0.3 [m/sec])
a_gd = 0.999;						% compensate gyro drift

k_phidot = 25;						% rotation speed gain
k_sync = 0.35;						% wheel synchronization gain

% données physiques, NE PAS MODIFIER
k_thetadot = 0.3 / R;				% speed gain (0.3 [m/sec])
k_phidot = 25;						% rotation speed gain
k_sync = 0.35;						% wheel synchronization gain
sound_freq = 440;					% sound frequency [Hz]
sound_dur =	500;					% sound duration [msec]
dst_thr = 20;						% distance threshold for obstacle avoidance [cm]
turn_angle = round(60 * W / R);		% right-turn angle in autonomous drive [deg]
gp_max = 100;						% maximum game pad input
log_count = 25;						% data logging count (logging sample time = ts1 * log_count)
% LocalWords:  QQ KK QQ KK msec Coulombic pwm


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
syms u theta psi dtheta dpsi real

x = [theta;psi;dtheta;dpsi];

% computes the value of the x dot vector (state derivative)
i = 1/Rm * ( u + Kb*(dpsi-dtheta) );
Ftheta = 2*( n*Kt*i + fm*(dpsi-dtheta) - fw*dtheta );
%Ftheta = n*Kt*i + fm*(dpsi-dtheta) - fw*dtheta;
Fpsi = -2*n*Kt*i - 2*fm*(dpsi-dtheta);
%Fpsi = -n*Kt*i - fm*(dpsi-dtheta);
M1 = [ ((2*m+M)*R^2+2*Jw+2*n^2*Jm)  (M*L*R*cos(psi)-2*n^2*Jm) ;
       (M*L*R*cos(psi)-2*n^2*Jm)    (M*L^2+Jpsi+2*n^2*Jm) ];
M2 = [ Ftheta+M*L*R*dpsi^2*sin(psi);
       Fpsi+M*g*L*sin(psi)];
var = M1\M2;

xdot1 = dtheta;
xdot2 = dpsi;
xdot3 = var(1);
xdot4 = var(2);

f = [xdot1;xdot2;xdot3;xdot4];


A = jacobian(f,x);
B = jacobian(f,u);

theta = 0;
psi = 0;
dtheta = 0;
dpsi = 0;
u = 0;



eval(f);


A = eval(A);
B = eval(B);

eig(A);

Aaug = [A zeros(4,1); -1 0 0 0 0];
Baug = [B; 0];

%Comande LQR
% Q = eye(5);
% Q(1,1) = 10;
% Q(2,2) = 50;
% R = 1;
% % 
% Kaug = lqr(Aaug,Baug,Q,R);

p1 = -2 + 2.10i;
p2 = -179.4329;
p3 = -2-2.10i;
p4 = -6.1443;
pint = -1;

Kaug = place(Aaug,Baug,[p1, p2, p3, p4, pint]); % -3 et -4 (petits acoups), -1 et -2 (plus gros acoups), -195.4279, -179.4329, -6.1443
K = Kaug(1:4);
Ki = Kaug(5);

C = [1 0 0 0; 0 0 0 1];


obs_desired_poles = [p1*15 p2*15 p3*15 p4*15];
L = place (A', C', obs_desired_poles);
L = L';

Abf = A - B*K;
C = [1 0 0 0; 0 0 0 1];
sysbf = ss(Abf, B, [1 0 0 0], 0);
dc_gain = dcgain(sysbf);
lc = 1/dc_gain;

B_virtual = 2*B2(:,2);
p5 = -1;
p6 = -68;

eig(A2);

K_rot = place(A2, B_virtual, [p5 p6]);
Abf2 = A2 - B_virtual*K_rot;
sysbf2 = ss(Abf2, B_virtual, [1 0],0);
dc_gain2 = dcgain(sysbf2);
lc2 = 1/dc_gain2;
% 
% 
% 
% 
% Qo = 1*eye(4);
% Qo(2,2) = 1000000;
% Ro = 1;
% L = lqr(A',C',Qo,Ro)';
% 
% 
% Eig_K = eig(A-B*K);
% Eig_L = eig(A-L*C);


% figure
% hold on
% plot(real(Eig_K),imag(Eig_K),'x','MarkerSize',20,'LineWidth',4)
% plot(real(Eig_L),imag(Eig_L),'x','MarkerSize',20,'LineWidth',4)
% 
% legend({'$\lambda(A-BK)$','$\lambda(A-LC)$'},'interpreter','latex')


