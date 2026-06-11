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
    def __init__(self, K, lc, ref_time, ref_ampl, time, mov_points):
        # Gain retour d'état
        self.K = K

        # Gaine de consigne
        self.lc = lc

        # Figure pour les courbes
        self.fig, self.ax = plt.subplots()

        # Figure pour le robot qui bouge
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 6))

        # Temps de début et fin d'animation
        self.tspan = (0.0, time)

        # Nombre d'images à afficher, dépend du temps finale
        self.frame_count = time*85

        # Intervalle de temps entre début et fin avec x images entre les 2
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=self.frame_count)

        # Début de l'échelon envoyé
        self.start_reference_time = ref_time

        # Amplitude de l'échelon
        self.initial_amplitude = ref_ampl

        # Valeur initiale des variables d'état
        self.x0 = [0.0, 0.0, 0.0, 0.0]

        # Valeur initiale de y, R*theta
        self.y = 0

        # Variable pour savoir la manière d'afficher les courbes
        self.update_point = mov_points
        self.next_moving_type = self.update_point

        # Simule une première fois le système non linéaire avec valeurs passées en argument
        self.run_simulation()
        
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


        # Variable pour mettre pause/play
        self.paused = True

        # Pour savoir quand la simulation est terminée
        self.simulation_end = True

        self.reset = True
        
        # Initialisation de l'animation des courbes, qui démarre quand on appuie sur a
        self.ani = None
        # Initialisation de l'animation du robot
        self.ani2 = None

        # Relier le fait de mettre sur pause et lancer la simulation lors d'appuis sur 'a' et espace
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_pause)
        self.fig2.canvas.mpl_connect('key_press_event', self.toggle_pause)

        self.fig.canvas.manager.set_window_title("Curves' animation")
        self.fig2.canvas.manager.set_window_title('Gyropode')


    # Simule le système non linéaire
    def run_simulation(self):
        self.sol = solve_ivp(nxt.xdot, self.tspan, self.x0, t_eval=self.t_eval, method='RK45', args=(self.K, self.lc, consigne_temp, self.start_reference_time, self.initial_amplitude))

        self.t = self.sol.t
        self.xout = self.sol.y
        self.theta_nlin = self.sol.y[0, :]
        self.psi_nlin = self.sol.y[1, :]

        self.command = np.zeros(len(self.t))

        self.y = R*self.theta_nlin

        self.yc = []
        for i in range(len(self.t)):
            yc_actuelle = consigne_temp(self.t[i], self.start_reference_time, self.initial_amplitude)
            x_actuelle = self.xout[:, i]
            utheo = -np.dot(self.K, x_actuelle) + yc_actuelle*self.lc
            utheo = np.clip(utheo, -8.0, 8.0)
            self.command[i] = utheo[0]
            self.yc.append(yc_actuelle)

        self.update_point = self.next_moving_type

    # Fonction qui met à jour notre animation en temps réel
    def update(self, frame):
        #Si la simulation se finit d'elle même
        if frame == self.frame_count - 1:
            #depassement = (max(self.theta_nlin[:frame]) - max(self.yc[:frame]))*100/(max(self.yc[:frame]))
            #maximum = np.max([np.max(self.command), np.max(self.yc), np.max(self.theta_nlin), np.max(self.psi_nlin)]) + 1
            # Voir pour passer ça sur une autre fenêtre
            #if depassement < 200:
            #    self.ax.text(0, maximum, f'Overshoot : {round(depassement,1)} %')
            self.paused = True
            self.simulation_end = True
        elif frame == 0:
            for txt in self.ax.texts:
                txt.set_visible(False)

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


    # Pour changer les paramètre de commande et relancer le solver
    def update_simu(self, K, lc, ref_time, ampl, end_time, mov_points):
        self.K = K
        self.lc = lc
        self.initial_amplitude = ampl
        self.start_reference_time = ref_time
        self.tspan = (0.0, end_time)
        self.frame_count = end_time*80
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=self.frame_count)
        self.next_moving_type = mov_points

    # Gestion de la mise en pause et recommencement (et fin d'animation)
    def toggle_pause(self, event):
        if event.key != ' ' and event.key != 'a': #Mettre pause que si on appuie sur espace et recommencer si on appuie sur a
            return
        elif event.key == ' ' and self.ani is not None and self.ani2 is not None and not self.reset:
            if self.paused and self.simulation_end == False:
                self.ani.resume()
                self.ani2.resume()
                self.paused = False
            elif self.simulation_end == False:
                self.ani.pause()
                self.ani2.pause()
                self.paused = True
        elif event.key == ' ' and (self.ani is None or self.ani2 is None or self.reset):
            self.paused = False
            self.run_simulation()
            maximum = np.max([np.max(self.command), np.max(self.yc), np.max(self.theta_nlin), np.max(self.psi_nlin)]) + 0.4
            minimum = np.min([np.min(self.command), np.min(self.yc), np.min(self.theta_nlin), np.min(self.psi_nlin)]) - 0.4
            self.ax.set(xlim=[0, self.tspan[1]], ylim=[minimum, maximum], xlabel='Time [s]', ylabel='Amplitude')
            self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=self.frame_count, interval=10, repeat=False, blit=True)
            self.fig.canvas.draw()
            self.ani2 = animation.FuncAnimation(fig=self.fig2, func=self.update2, frames=self.frame_count, interval=10, repeat=False, blit=True)
            self.fig2.canvas.draw()
            self.simulation_end = False
            self.reset = False
        elif event.key == 'a':
            if self.paused == True:
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

                self.fig.canvas.draw()
                self.fig2.canvas.draw()
                self.reset = True            


#anim = MyAnimation(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, 1, -1, 3, 'Moving curves')
#plt.show()