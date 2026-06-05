import numpy as np
import math

# Parameters of the  two-wheel robot

# Physical Constant

g = 9.81  # gravity acceleration [m/sec^2]

# Lego Mindstorms EV3 Parameters
m = 0.03  # wheel weight [kg] valor inicial 0.03
R = 0.042  # wheel radius [m]  valor inicial 0.04
Jw = m * R ** 2 / 2  # wheel inertia moment [kgm^2]
M = 0.67  # body weight [kg]
W = 0.165  # body width [m]
D = 0.05  # body depth [m]
H = 0.152  # body height [m]
L = H / 2  # distance of the center of mass from the wheel axle [m]
Jpsi = M * L ** 2 / 3  # body pitch inertia moment [kgm^2]
Jphi = M * (W ** 2 + D ** 2) / 12  # body yaw inertia moment [kgm^2]
fm = 0.0022  # friction coefficient between body & DC motor
fw = 0  # friction coefficient between wheel & floor

# DC Motor Parameters

Jm = 1e-5  # DC motor inertia moment [kgm^2]
Rm = 6.8327  # DC motor resistance [ƒ¶]
Kb = 0.468  # DC motor back EMF constant [Vsec/rad]
Kt = 0.3047  # DC motor torque constant [Nm/A]
n = 1  # gear ration

beta = n * Kt * Kb / Rm + fm
alpha = n * Kt / Rm
tmp = beta + fw


# Parametre de la fonction :
# t : le temps de simulation
# x : l'état à un instant t
# Kin : le gain de retour d'état
# lcin : le prégain
# yc : la consigne à un instant t : une fontion qui prend en argument les 2 suivant :
# start_time : le temps de début de l'échelon
# amplitude : l'amplitude de l'échelon en entrée

# Paramère de sortie : xdot

def xdot(t, xin, Kin, lcin, yc, start_time_input, amplitude):
    # positionvector
    theta = xin[0]  # angular position of thewheel
    psi = xin[1]  # angular positionof the gyropode
    # speedvector
    dtheta = xin[2]  # angular speed of thewheel
    dpsi = xin[3]  # angularspeed of the gyropode

    # compute u
    x = np.reshape(xin, (4, 1))
    uth = -(np.dot(Kin, x)) + lcin * yc(t, start_time_input, amplitude)
    uth = uth[0, 0]
    u = np.clip(uth, -8.0, 8.0)

    # computes the value of the x dot vector (state derivative)

    i = 1 / Rm * (u + Kb * (dpsi - dtheta))

    Ftheta = 2 * alpha * u - 2 * beta * (dtheta - dpsi) - 2 * fw * dtheta

    Fpsi = -2 * alpha * u + 2 * beta * (dtheta - dpsi)

    M1 = np.array([[(2 * m + M) * R ** 2 + 2 * Jw + 2 * n ** 2 * Jm, M * L * R * math.cos(psi) - 2 * n ** 2 * Jm],
                   [M * L * R * math.cos(psi) - 2 * n ** 2 * Jm, M * L ** 2 + Jpsi + 2 * n ** 2 * Jm]])
    M2 = np.array([[Ftheta + M * L * R * dpsi ** 2 * math.sin(psi)],
                   [Fpsi + M * g * L * math.sin(psi)]])

    var = np.linalg.solve(M1, M2)

    xdot1 = dtheta
    xdot2 = dpsi
    xdot3 = var[0, 0]
    xdot4 = var[1, 0]

    return [xdot1, xdot2, xdot3, xdot4]