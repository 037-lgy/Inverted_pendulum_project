import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import NXTwaysim as nxt
from scipy.integrate import solve_ivp
import BE_script as be


class MyAnimation:
    def __init__(self, K, lc, reference, ref_time, ref_ampl):
        self.K = K
        self.lc = lc
        self.consigne_temp = reference

        self.fig, self.ax = plt.subplots()

        self.tspan = (0.0, 2.0)
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=200)
        self.start_reference_time = ref_time
        self.start_amplitude = ref_ampl

        self.x0 = [0.0, 0.0, 0.0, 0.0]
        self.sol = solve_ivp(nxt.xdot, self.tspan, self.x0, t_eval=self.t_eval, method='RK45', args=(self.K, self.lc, self.consigne_temp, self.start_reference_time, self.start_amplitude))

        self.t = self.sol.t
        self.xout = self.sol.y
        self.theta_nlin = self.sol.y[0, :]
        self.psi_nlin = self.sol.y[1, :]

        self.command = np.zeros(len(self.t))

        self.yc = []
        for i in range(len(self.t)):
            yc_actuelle = be.consigne_temp(self.t[i], self.start_reference_time, self.start_amplitude)
            x_actuelle = self.xout[:, i]
            utheo = -np.dot(self.K, x_actuelle) + yc_actuelle*self.lc
            utheo = np.clip(utheo, -8.0, 8.0)
            self.command[i] = utheo[0]
            self.yc.append(yc_actuelle)

        self.line1 = self.ax.plot(self.t[0], self.command[0], label='u')[0]
        self.line2 = self.ax.plot(self.t[0], self.theta_nlin[0], label='theta')[0]
        self.line3 = self.ax.plot(self.t[0], self.psi_nlin[0], label='psi')[0]
        self.line4 = self.ax.plot(self.t[0], self.yc[0], label='yc')[0]
        self.ax.set(xlim=[0, 2], ylim=[-5, 5], xlabel='Time [s]', ylabel='Amplitude')
        self.ax.legend()

        self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=400, interval=10, repeat=False)
        self.paused = False

        self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)


    def update(self, frame):
        # update the line plot:
        self.line1.set_xdata(self.t[:frame])
        self.line1.set_ydata(self.command[:frame])
        self.line2.set_xdata(self.t[:frame])
        self.line2.set_ydata(self.theta_nlin[:frame])
        self.line3.set_xdata(self.t[:frame])
        self.line3.set_ydata(self.psi_nlin[:frame])
        self.line4.set_xdata(self.t[:frame])
        self.line4.set_ydata(self.yc[:frame])
        return (self.line1, self.line2, self.line3, self.line4)
    

    def reset_simu(self, K, lc, reference):
        self.K = K
        self.lc = lc
        self.consigne_temp = reference
        self.sol = solve_ivp(nxt.xdot, self.tspan, self.x0, t_eval=self.t_eval, method='RK45', args=(self.K, self.lc, self.consigne_temp, self.start_reference_time, self.start_amplitude))

        self.t = self.sol.t
        self.xout = self.sol.y
        self.theta_nlin = self.sol.y[0, :]
        self.psi_nlin = self.sol.y[1, :]

        self.command = np.zeros(len(self.t))

        self.yc = []
        for i in range(len(self.t)):
            yc_actuelle = be.consigne_temp(self.t[i], self.start_reference_time, self.start_amplitude)
            x_actuelle = self.xout[:, i]
            utheo = -np.dot(self.K, x_actuelle) + yc_actuelle*self.lc
            utheo = np.clip(utheo, -8.0, 8.0)
            self.command[i] = utheo[0]
            self.yc.append(yc_actuelle)

        self.line1 = self.ax.plot(self.t[0], self.command[0], label='u')[0]
        self.line2 = self.ax.plot(self.t[0], self.theta_nlin[0], label='theta')[0]
        self.line3 = self.ax.plot(self.t[0], self.psi_nlin[0], label='psi')[0]
        self.line4 = self.ax.plot(self.t[0], self.yc[0], label='yc')[0]
        self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=400, interval=10, repeat=False)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
            self.reset_simu(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, self.consigne_temp)
        self.paused = not self.paused


# Frame : le nombre d'images qui sont générées
# Intervale : le temps entre 2 frames en ms normalement mais dépend du pc
# repeat : est-ce qu'on répète la simu quand toutes les frames ont été display
# blit : qualité de l'image je crois

# update : la fonction qui est appelée tous les intervalles


# fig, ax = plt.subplots()

# tspan = (0.0, 2.0)
# t_eval = np.linspace(tspan[0], tspan[1], num=200)

# K = np.array([[-5.5148, -34.12178, -1.7862, -2.8974]])
# lc = -5.5148
# start_reference_time = 0
# start_amplitude = 1

# x0 = [0.0, 0.0, 0.0, 0.0]
# sol = solve_ivp(nxt.xdot, tspan, x0, t_eval=t_eval, method='RK45', args=(K, lc, be.consigne_temp, start_reference_time, start_amplitude))

# t = sol.t
# xout = sol.y
# theta_nlin = sol.y[0, :]
# psi_nlin = sol.y[1, :]

# command = np.zeros(len(t))

# yc = []
# for i in range(len(t)):
#     yc_actuelle = be.consigne_temp(t[i], start_reference_time, start_amplitude)
#     x_actuelle = xout[:, i]
#     utheo = -np.dot(K, x_actuelle) + yc_actuelle*lc
#     utheo = np.clip(utheo, -8.0, 8.0)
#     command[i] = utheo[0]
#     yc.append(yc_actuelle)

# line1 = ax.plot(t[0], command[0], label='u')[0]
# line2 = ax.plot(t[0], theta_nlin[0], label='theta')[0]
# line3 = ax.plot(t[0], psi_nlin[0], label='psi')[0]
# line4 = ax.plot(t[0], yc[0], label='yc')[0]
# ax.set(xlim=[0, 2], ylim=[-2.5, 2.5], xlabel='Time [s]', ylabel='Amplitude')
# ax.legend()

# def update(frame):
#     # update the line plot:
#     line1.set_xdata(t[:frame])
#     line1.set_ydata(command[:frame])
#     line2.set_xdata(t[:frame])
#     line2.set_ydata(theta_nlin[:frame])
#     line3.set_xdata(t[:frame])
#     line3.set_ydata(psi_nlin[:frame])
#     line4.set_xdata(t[:frame])
#     line4.set_ydata(yc[:frame])
#     return (line1, line2, line3, line4)


# ani = animation.FuncAnimation(fig=fig, func=update, frames=400, interval=10, repeat=False)
# plt.show()

anim = MyAnimation(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, be.consigne_temp, 0, 1)
plt.show()