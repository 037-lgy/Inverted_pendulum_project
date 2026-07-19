import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

import control as ctrl

from scipy.integrate import solve_ivp
import math

# Parameters of the  two-wheel robot

# Physical Constant

g = 9.81  # gravity acceleration [m/sec^2]

# Lego Mindstorms EV3 Parameters
m = 0.03  # wheel weight [kg] valor inicial 0.03
R = 0.042  # wheel radius [m]  valor inicial 0.04
Jw = m * R**(2) / 2  # wheel inertia moment [kgm^2]

####################################################################
M = 0.8  # body weight [kg] 
W = 0.042  # body width [m]
D = 0.055  # body depth [m]
H = 0.160  # body height [m]

####################################################################
L = H / 2  # distance of the center of mass from the wheel axle [m]
Jpsi = M * L ** 2 / 3  # body pitch inertia moment [kgm^2]
Jphi = M * (W ** 2 + D ** 2) / 12  # body yaw inertia moment [kgm^2]
fm = 0.0022  # friction coefficient between body & DC motor
fw = 0  # friction coefficient between wheel & floor

# DC Motor Parameters

Jm = 1e-5  # DC motor inertia moment [kgm^2]

###################################################################
Rm = 6.69  # DC motor resistance [ƒ¶]
Kb = 0.468  # DC motor back EMF constant [Vsec/rad]
###################################################################
Kt = 0.317  # DC motor torque constant [Nm/A]
###################################################################
n = 1  # gear ration

beta = n * Kt * Kb / Rm + fm
alpha = n * Kt / Rm
tmp = beta + fw

H = 0.160
R = 0.042
r = 0.01

def xdot_segment(t, xin, Kin, lcin, yc):
    # positionvector
    theta = xin[0]  # angular position of thewheel
    psi = xin[1]  # angular positionof the gyropode
    # speedvector
    dtheta = xin[2]  # angular speed of thewheel
    dpsi = xin[3]  # angularspeed of the gyropode

    # compute u
    x = np.reshape(xin, (4, 1))
    uth = -(np.dot(Kin, x)) + lcin * yc
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

class MyAnimation:
    def __init__(self, K, lc, ref_ampl, time, mov_points):
        # Gain retour d'état
        self.K = K

        # Gaine de consigne
        self.lc = lc

        # Temps de début et fin d'animation
        self.tspan = (0.0, time)

        # Nombre d'images à afficher, dépend du temps finale
        self.frame_count = time*85

        # Intervalle de temps entre début et fin avec x images entre les 2
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=self.frame_count)

        # Amplitude de l'échelon
        self.initial_amplitude = ref_ampl

        # Valeur initiale des variables d'état
        self.x0 = [0.0, 0.0, 0.0, 0.0]

        # Variable pour savoir la manière d'afficher les courbes
        self.update_point = mov_points

        # Simule une première fois le système non linéaire avec valeurs passées en argument
        self.run_simulation()

        # --- Figure 1 : Les courbes ---

        self.fig, self.ax = plt.subplots()
        
        # Initialise les courbes à afficher et la figure
        self.line1 = self.ax.plot([0], [0], label='u', color='b', linewidth=1)[0]
        self.line2 = self.ax.plot([0], [0], label='theta', color='r', linewidth=1)[0]
        self.line3 = self.ax.plot([0], [0], label='psi', color='g', linewidth=1)[0]
        self.line4 = self.ax.plot([0], [0], label='yc', color='y', linewidth=1)[0]
        
        # Initialise les points à afficher
        self.point1 = self.ax.plot([], [], ls="none", marker="o", color='b', markersize=3)[0]
        self.point2 = self.ax.plot([], [], ls="none", marker='o', color='r', markersize=3)[0]
        self.point3 = self.ax.plot([], [], ls="none", marker='o', color='g', markersize=3)[0]
        self.point4 = self.ax.plot([], [], ls="none", marker='o', color='y', markersize=3)[0]

        # Initialise les bornes des axes en fonction de la valeur des courbes
        maximum = np.max([np.max(self.command), np.max(self.yc), np.max(self.theta_nlin), np.max(self.psi_nlin)]) + 0.4
        minimum = np.min([np.min(self.command), np.min(self.yc), np.min(self.theta_nlin), np.min(self.psi_nlin)]) - 0.4
        self.ax.set(xlim=[0, self.tspan[1]], ylim=[minimum, maximum], xlabel='Time [s]', ylabel='Amplitude')
        self.ax.legend()

        # --- Figure 2 : Le robot ---
        
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))

        self.round = np.arange(0, 2*np.pi, 0.1)
        self.y_initial = 0
        self.A_init = [self.y_initial, 0]
        self.B_init = [self.A_init[0], R]
        self.C_init = [self.B_init[0]+H*np.sin(self.x0[1]), self.B_init[1]+H*np.cos(self.x0[1])]

        # Initialise les parties du robot à afficher
        self.uppermass = self.ax2.plot(self.C_init[0]+r*np.cos(self.round), self.C_init[1]+r*np.sin(self.round), 'r', linewidth=2)[0]
        self.wheelmark = self.ax2.plot([self.B_init[0], self.B_init[0]+R*np.sin(self.x0[0])], [self.B_init[1], self.B_init[1]+R*np.cos(self.x0[0])], 'b-', linewidth=2)[0]
        self.rod = self.ax2.plot([self.B_init[0], self.C_init[0]], [self.B_init[1], self.C_init[1]], 'r-', linewidth=3)[0]
        self.wheel = self.ax2.plot(self.B_init[0]+R*np.cos(self.round), self.B_init[1]+R*np.sin(self.round), 'r', linewidth=2)[0]
        # Simulation time
        self.printtime = self.ax2.text(-0.3, 0.3, f'Simulation time : {str(0)}', fontsize=12)
        # Le sol en dessous
        self.ax2.plot([-5, 5], [0, 0], 'k-', linewidth=1.5)
        self.ax2.set(xlim=[-1.2, 1.2], ylim=[-0.15, 0.4], title='Animation of the NXTway', aspect='equal')
        self.ax2.grid(True)
        
        # Création des animations dès le départ
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=self.frame_count,
            interval=10,
            repeat=False,
            blit=False
        )

        self.ani2 = animation.FuncAnimation(
            self.fig2,
            self.update2,
            frames=self.frame_count,
            interval=10,
            repeat=False,
            blit=False
        )

        plt.close(self.fig)
        plt.close(self.fig2)


    # Simule le système non linéaire
    def run_simulation(self):
        self.sol = solve_ivp(xdot_segment, self.tspan, self.x0, t_eval=self.t_eval, method='RK45', args=(self.K, self.lc, self.initial_amplitude))

        self.t = self.sol.t
        self.xout = self.sol.y
        self.theta_nlin = self.sol.y[0, :]
        self.psi_nlin = self.sol.y[1, :]

        self.command = np.zeros(len(self.t))

        self.y = R*self.theta_nlin

        self.yc = [self.initial_amplitude] * len(self.t)
        
        for i in range(len(self.t)):
            x_actuelle = self.xout[:, i]
            utheo = -np.dot(self.K, x_actuelle) + self.yc[i]*self.lc
            utheo = np.clip(utheo, -8.0, 8.0)
            self.command[i] = utheo[0]

    # Fonction qui met à jour notre animation en temps réel
    def update(self, frame):
        
        # Mise à jour des courbes à afficher:

        if self.update_point == 'Moving points':
            if frame == 0:
                self.line1.set_xdata(self.t[:self.frame_count])
                self.line1.set_ydata(self.command[:self.frame_count])
                self.line2.set_xdata(self.t[:self.frame_count])
                self.line2.set_ydata(self.theta_nlin[:self.frame_count])
                self.line3.set_xdata(self.t[:self.frame_count])
                self.line3.set_ydata(self.psi_nlin[:self.frame_count])
                self.line4.set_xdata(self.t[:self.frame_count])
                self.line4.set_ydata(self.yc[:self.frame_count])


            self.point1.set_xdata([self.t[frame]])
            self.point1.set_ydata([self.command[frame]])
            self.point2.set_xdata([self.t[frame]])
            self.point2.set_ydata([self.theta_nlin[frame]])
            self.point3.set_xdata([self.t[frame]])
            self.point3.set_ydata([self.psi_nlin[frame]])
            self.point4.set_xdata([self.t[frame]])
            self.point4.set_ydata([self.yc[frame]])
        
        elif self.update_point == 'Moving curves':
            self.line1.set_xdata(self.t[:frame])
            self.line1.set_ydata(self.command[:frame])
            self.line2.set_xdata(self.t[:frame])
            self.line2.set_ydata(self.theta_nlin[:frame])
            self.line3.set_xdata(self.t[:frame])
            self.line3.set_ydata(self.psi_nlin[:frame])
            self.line4.set_xdata(self.t[:frame])
            self.line4.set_ydata(self.yc[:frame])

        else:
            if frame == 0:
                self.line1.set_xdata(self.t[:self.frame_count])
                self.line1.set_ydata(self.command[:self.frame_count])
                self.line2.set_xdata(self.t[:self.frame_count])
                self.line2.set_ydata(self.theta_nlin[:self.frame_count])
                self.line3.set_xdata(self.t[:self.frame_count])
                self.line3.set_ydata(self.psi_nlin[:self.frame_count])
                self.line4.set_xdata(self.t[:self.frame_count])
                self.line4.set_ydata(self.yc[:self.frame_count])


            self.point1.set_xdata([self.t[:frame]])
            self.point1.set_ydata([self.command[:frame]])
            self.point2.set_xdata([self.t[:frame]])
            self.point2.set_ydata([self.theta_nlin[:frame]])
            self.point3.set_xdata([self.t[:frame]])
            self.point3.set_ydata([self.psi_nlin[:frame]])
            self.point4.set_xdata([self.t[:frame]])
            self.point4.set_ydata([self.yc[:frame]])

        return (self.line1, self.line2, self.line3, self.line4, self.point1, self.point2, self.point3, self.point4)
    
    def update2(self, frame):
        A = [self.y[frame], 0]
        B = [A[0], R]
        C = [B[0]+H*np.sin(self.psi_nlin[frame]), B[1]+H*np.cos(self.psi_nlin[frame])]

        self.uppermass.set_data(C[0]+r*np.cos(self.round), C[1]+r*np.sin(self.round))
        self.wheelmark.set_data([B[0], B[0]+R*np.sin(self.theta_nlin[frame])], [B[1], B[1]+R*np.cos(self.theta_nlin[frame])])
        self.rod.set_data([B[0], C[0]], [B[1], C[1]])
        self.wheel.set_data(B[0]+R*np.cos(self.round), B[1]+R*np.sin(self.round))
        self.printtime.set_text(f'Simulation time : {round(self.t_eval[frame], 2)}')

        return(self.uppermass, self.wheelmark, self.rod, self.wheel, self.printtime)