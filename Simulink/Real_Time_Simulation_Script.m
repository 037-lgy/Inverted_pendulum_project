clear all
close all
clc

ts1 = 0.004;						% ts1 sample time [sec]

time_start = 1250;                  % start time of balancing [msec] (= gyro calibration time)

a_gc = 0.8;							% calibrate gyro offset

a_b = 0.8;							% average battery value

a_d = 0.8;							% suppress velocity noise

a_gd = 0.999;						% compensate gyro drift

pwm_gain = 1;						% pwm gain
pwm_offset = 0;						% pwm offset

BATTERY = 8000;						% initial value of battery [mV]