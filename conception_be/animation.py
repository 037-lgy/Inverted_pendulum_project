import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import NXTwaysim as nxt
import control as ctrl
from control import matlab
from scipy.integrate import solve_ivp

A = np.array([[0, 0, 1, 0], 
              [0, 0, 0, 1], 
              [0, -413.51141165, -131.57981958, 131.57981958], 
              [0, 265.56666878, 62.72534683, -62.72534683]])

B = np.array([[0], [0], [254.34231643], [-121.24739236]])

A = np.array([[0, 0, 1, 0], 
              [0, 0, 0, 1], 
              [0, -444.58852126, -123.11348321, 123.11348321], 
              [0, 264.94676359, 55.09518151, -55.09518151]])

B = np.array([[0], [0], [239.3206408], [-107.09967584]])

C = np.array([1, 0, 0, 0])
    
def compute_K_lc(wn, z):
    if z < 1:
        imag_part = ((4*wn**2-4*z**2*wn**2)**(1/2)) / 2
        p1 = complex(-wn*z, imag_part)
        p2 = np.conj(p1)

    elif z == 1:
        eps = 0.000001
        p1 = -wn + eps
        p2 = -wn - eps
    else:
        real_part_p1 = -z*wn + wn*((z**2 - 1)**(0.5))
        real_part_p2 = -z*wn - wn*((z**2 - 1)**(0.5))
        p1 = complex(real_part_p1, 0)
        p2 = complex(real_part_p2, 0)
    p3 = 5*p2.real
    p4 = 5*p2.real - 0.5
    p_desired = [p1, p2, p3, p4]
    K = matlab.place(A,B, p_desired)


    ACL = np.dot(B, K)
    ACL = A - ACL
    BCL = B
    CCL = C

    sysGCL = ctrl.ss(ACL, BCL, CCL, 0)

    dc_gain = ctrl.dcgain(sysGCL)
    lc = 1 / dc_gain
    return (K, lc)

def consigne_temp(t, start_time, amplitude):
    if t < start_time:
        return 0
    else:
        return amplitude
    
H = 0.160
R = 0.042
r = 0.01

class MyAnimation:
    def __init__(self, K, lc, ref_ampl, time, mov_points):
        # Gain retour d'état
        self.K = K

        # Gaine de consigne
        self.lc = lc

        self.fig, self.ax = plt.subplots()

        # Figure pour le robot qui bouge
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))

        # Amplitude de l'échelon
        self.current_yc = ref_ampl

        self.time = time

        self.dt = 0.001
        self.steps_per_frame = 20

        self.current_t = 0

        # Valeur initiale des variables d'état
        self.x0 = [0.0, 0.0, 0.0, 0.0]

        # Valeur initiale de y, R*theta
        self.x = [0, 0, 0, 0]
        self.theta_nlin = 0
        self.psi_nlin = 0
        self.y = 0

        self.previous_x = self.x

        self.x_history = [0]
        self.theta_history = [0]
        self.psi_history = [0]
        self.t_history = [0]
        self.u_history = [0]
        self.yc_history = [0]

        self.reference = 0

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
        self.ax.set(xlim=[0, self.time], ylim=[-8, 8], xlabel='Time [s]', ylabel='Amplitude')
        self.ax.grid(True)
        self.ax.legend()

        self.moving_type = 'Moving curves'

        self.round = np.arange(0, 2*np.pi, 0.1)
        self.A_init = [self.y, 0]
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


        # Variable pour mettre pause/play
        self.paused = True

        self.reset = True

        self.ani2 = animation.FuncAnimation(fig=self.fig2, func=self.update2, interval=10, repeat=False, blit=False, cache_frame_data=False)
        self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, interval=10, repeat=False, blit=False, cache_frame_data=False)
        self.ani.pause()
        self.ani2.pause()
        self.started = False
        # Relier le fait de mettre sur pause et lancer la simulation lors d'appuis sur 'a' et espace
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_pause)
        self.fig2.canvas.mpl_connect('key_press_event', self.toggle_pause)

        self.fig2.canvas.manager.set_window_title('Gyropode')
        self.fig.canvas.manager.set_window_title("Curves' plot")

    def compute_simulation(self):
        for _ in range(self.steps_per_frame):
            self.current_t += self.dt
            dx = nxt.xdot_segment(self.current_t, self.previous_x, self.K, self.lc, self.current_yc)
            self.x = [self.previous_x[i] + self.dt * dx[i] for i in range(4)]
            self.previous_x = self.x
        
        self.theta_nlin = self.x[0]
        self.psi_nlin = self.x[1]
        self.y = R*self.theta_nlin

        self.t_history.append(self.current_t)
        self.theta_history.append(self.theta_nlin)
        self.psi_history.append(self.psi_nlin)
        self.yc_history.append(self.current_yc)

        u = 0
        for i in range(4):
            u = -self.K[0,i]*self.x[i] + u
        u = u + self.current_yc*self.lc
        if u < -8:
            u = -8
        elif u > 8:
            u = 8
        self.u_history.append(u)

    def update(self, frame):
        if not self.started:
            return (self.line1, self.line2, self.line3, self.line4)

        if len(self.t_history) <= 1:

            self.line1.set_xdata(self.t_history)
            self.line1.set_ydata(self.u_history)
            self.line2.set_xdata(self.t_history)
            self.line2.set_ydata(self.theta_history)
            self.line3.set_xdata(self.t_history)
            self.line3.set_ydata(self.psi_history)
            self.line4.set_xdata(self.t_history)
            self.line4.set_ydata(self.yc_history)


            return (self.line1, self.line2, self.line3, self.line4)
        
        t_arr = np.array(self.t_history)
        u_arr = np.array(self.u_history)
        theta_arr = np.array(self.theta_history)
        psi_arr = np.array(self.psi_history)
        yc_arr = np.array(self.yc_history)

        t_now = t_arr[-1]
        window_start_threshold = self.time-1 if self.time < 5 else self.time-2
        if t_now <= window_start_threshold:
            xlim_min, xlim_max = 0, self.time
        else:
            xlim_min, xlim_max = t_now - window_start_threshold, t_now - window_start_threshold + self.time

        mask = (t_arr >= xlim_min) & (t_arr <= xlim_max)
        maximum = np.max([np.max(u_arr[mask]), np.max(yc_arr[mask]), np.max(theta_arr[mask]), np.max(psi_arr[mask])]) + 0.4
        minimum = np.min([np.min(u_arr[mask]), np.min(yc_arr[mask]), np.min(theta_arr[mask]), np.min(psi_arr[mask])]) - 0.4

        self.ax.set_xlim(xlim_min, xlim_max)
        self.ax.set_ylim(minimum, maximum)
        self.line1.set_xdata(t_arr[mask])
        self.line1.set_ydata(u_arr[mask])
        self.line2.set_xdata(t_arr[mask])
        self.line2.set_ydata(theta_arr[mask])
        self.line3.set_xdata(t_arr[mask])
        self.line3.set_ydata(psi_arr[mask])
        self.line4.set_xdata(t_arr[mask])
        self.line4.set_ydata(yc_arr[mask])


        return (self.line1, self.line2, self.line3, self.line4)


    def update2(self, frame):
        if not self.started:
            return(self.uppermass, self.wheelmark, self.rod, self.wheel, self.printtime)
        self.compute_simulation()
        A = [self.y, 0]
        B = [A[0], R]
        C = [B[0]+H*np.sin(self.psi_nlin), B[1]+H*np.cos(self.psi_nlin)]

        self.uppermass.set_data(C[0]+r*np.cos(self.round), C[1]+r*np.sin(self.round))
        self.wheelmark.set_data([B[0], B[0]+R*np.sin(self.theta_nlin)], [B[1], B[1]+R*np.cos(self.theta_nlin)])
        self.rod.set_data([B[0], C[0]], [B[1], C[1]])
        self.wheel.set_data(B[0]+R*np.cos(self.round), B[1]+R*np.sin(self.round))
        self.printtime.set_text(f'Simulation time : {round(self.current_t, 2)}')
        self.previous_x = self.x

        return(self.uppermass, self.wheelmark, self.rod, self.wheel, self.printtime)


    # Pour changer les paramètre de commande et relancer le solver
    def update_simu(self, K, lc, ampl, end_time, mov_points):
        self.K = K
        self.lc = lc
        self.current_yc = ampl
        self.reference = ampl
        self.time = end_time


    # Gestion de la mise en pause et recommencement (et fin d'animation)
    def toggle_pause(self, event):
        if event.key != ' ' and event.key != 'a': #Mettre pause que si on appuie sur espace et recommencer si on appuie sur a
            return
        
        if event.key == ' ' :
            if not self.started:
                self.started = True
                self.paused = False
            elif self.paused:
                self.ani2.resume()
                self.ani.resume()
                self.paused = False
            else:
                self.ani2.pause()
                self.ani.pause()
                self.paused = True
        elif event.key == 'a':
            if self.paused == True:
                self.x = [0, 0, 0, 0]
                self.theta_nlin = 0
                self.psi_nlin = 0
                self.y = 0
                self.previous_x = self.x
                self.current_yc = self.reference
                self.current_t = 0

                self.x_history = [0]
                self.theta_history = [0]
                self.psi_history = [0]
                self.t_history = [0]
                self.u_history = [0]
                self.yc_history = [0]

                self.line1.set_data([], [])
                self.line2.set_data([], [])
                self.line3.set_data([], [])
                self.line4.set_data([], [])
                self.point1.set_data([], [])
                self.point2.set_data([], [])
                self.point3.set_data([], [])
                self.point4.set_data([], [])


                self.uppermass.set_data([], [])
                self.wheelmark.set_data([], [])
                self.rod.set_data([], [])
                self.wheel.set_data([], [])
                self.printtime.set_text('')

                self.uppermass = self.ax2.plot(self.C_init[0]+r*np.cos(self.round), self.C_init[1]+r*np.sin(self.round), 'r', linewidth=2)[0]
                self.wheelmark = self.ax2.plot([self.B_init[0], self.B_init[0]+R*np.sin(self.x0[0])], [self.B_init[1], self.B_init[1]+R*np.cos(self.x0[0])], 'b-', linewidth=2)[0]
                self.rod = self.ax2.plot([self.B_init[0], self.C_init[0]], [self.B_init[1], self.C_init[1]], 'r-', linewidth=3)[0]
                self.wheel = self.ax2.plot(self.B_init[0]+R*np.cos(self.round), self.B_init[1]+R*np.sin(self.round), 'r', linewidth=2)[0]
                self.printtime = self.ax2.text(-0.3, 0.3, f'Simulation time : {str(0)}', fontsize=12)

                self.fig2.canvas.draw()
                self.fig.canvas.draw()          


#anim = MyAnimation(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, 1, -1, 3, 'Moving curves')
#plt.show()