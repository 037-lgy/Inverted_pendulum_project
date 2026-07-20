% Simulation and Virtual Reality Parameters

% Copyright 2011 The MathWorks, Inc.

% Initial Values
PSI0 = 5 * pi / 180;				% initial value of body angle
X1IV = [							% x1 initial value
	0
	PSI0
	0
	0
	];
X2IV = [							% x2 initial value
	0
	0
	];

% Sample Rates
TS = 0.001;							% base sample rate [sec]

% Environments
GYRO0 = 600;						% initial value of gyro sensor
BATTERY = 8000;						% initial value of battery [mV]

% MAP
START_POS = [100, 100];				% initial position ([z, x]) [cm]

% condicoes adicionas por mim. verficar melhorias

% Conditions for Stopping Simulation
BODY_ANGLE_MAX = 15;				% maximum body angle
BODY_ANGLE_MIN = -15;				% minimum body angle

% Virtual Reality Parameters
TS_VR = 0.1;						% VRML refresh rate [sec]
BODY_HEIGHT = 13.2;					% NXTway body height [cm]				
CAMERA_HEIGHT = 13.2;				% camera height [cm]
CAMERA_DISTANCE = 50;				% distance between NXTway and camera [cm]
CAMERA_OFFSET = -8;					% z offset of Chaser View Point [cm]
ROTATION_X = [1, 0, 0];				% rotation vector around x axis
ROTATION_Y = [0, 1, 0];				% rotation vector around y axis


