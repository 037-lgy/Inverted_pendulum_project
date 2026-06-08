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

C = np.array([1, 0, 0, 0])
    
def compute_K_lc(wn, z):
    imag_part = ((4*wn**2-4*z**2*wn**2)**(1/2)) / 2
    p1 = complex(-wn*z, imag_part)
    p2 = np.conj(p1)
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
    

class MyAnimation:
    def __init__(self, K, lc, ref_time, ref_ampl, time):
        self.K = K
        self.lc = lc

        self.depassement = 0

        self.fig, self.ax = plt.subplots()

        self.tspan = (0.0, time)
        self.frame_count = 200 # Nombre d'images affichées
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=self.frame_count)
        self.start_reference_time = ref_time
        self.initial_amplitude = ref_ampl

        self.x0 = [0.0, 0.0, 0.0, 0.0]

        # Simule une première fois le système non linéaire avec valeurs passées en argument
        self.run_simulation()
        
        # Initialise les courbes à afficher et la figure
        self.line1 = self.ax.plot([0], [0], label='u')[0]
        self.line2 = self.ax.plot([0], [0], label='theta')[0]
        self.line3 = self.ax.plot([0], [0], label='psi')[0]
        self.line4 = self.ax.plot([0], [0], label='yc')[0]
        self.ax.set(xlim=[0, self.tspan[1]], ylim=[min(-8,-self.initial_amplitude), max(8,self.initial_amplitude)], xlabel='Time [s]', ylabel='Amplitude')
        self.ax.legend()

        # Commence par rien n'afficher
        self.paused = True

        # Pour savoir quand la simulation est terminée
        self.simulation_end = False
        
        # Pour permettre au premier déclenchement de se faire lors du premier appuie sur espace
        self.ani = None


        # Relier le fait de mettre sur pause et relancer avec espace
        #Il faudra relier l'appel de update simu au changement d'interface graphique
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_pause)
        plt.show()

    # Simulation non linéaire du système définit par les attributs
    def run_simulation(self):
        self.sol = solve_ivp(nxt.xdot, self.tspan, self.x0, t_eval=self.t_eval, method='RK45', args=(self.K, self.lc, consigne_temp, self.start_reference_time, self.initial_amplitude))

        self.t = self.sol.t
        self.xout = self.sol.y
        self.theta_nlin = self.sol.y[0, :]
        self.psi_nlin = self.sol.y[1, :]

        self.command = np.zeros(len(self.t))

        self.yc = []
        for i in range(len(self.t)):
            yc_actuelle = consigne_temp(self.t[i], self.start_reference_time, self.initial_amplitude)
            x_actuelle = self.xout[:, i]
            utheo = -np.dot(self.K, x_actuelle) + yc_actuelle*self.lc
            utheo = np.clip(utheo, -8.0, 8.0)
            self.command[i] = utheo[0]
            self.yc.append(yc_actuelle)

    # Fonction qui met à jour notre animation en temps réel
    def update(self, frame):
        #Si la simulation se finit d'elle même
        if frame == self.frame_count - 1:
            depassement = (max(self.theta_nlin[:frame]) - max(self.yc[:frame]))*100
            # Voir pour passer ça sur une autre fenêtre
            if depassement < 200:
                self.ax.text(0, max(8,self.initial_amplitude) + 1, f'Overshoot : {round(depassement,1)} %')
            self.paused = True
            self.simulation_end = True
        elif frame == 0:
            for txt in self.ax.texts:
                txt.set_visible(False)
                
        # Mise à jour des courbes à afficher:
        self.line1.set_xdata(self.t[:frame])
        self.line1.set_ydata(self.command[:frame])
        self.line2.set_xdata(self.t[:frame])
        self.line2.set_ydata(self.theta_nlin[:frame])
        self.line3.set_xdata(self.t[:frame])
        self.line3.set_ydata(self.psi_nlin[:frame])
        self.line4.set_xdata(self.t[:frame])
        self.line4.set_ydata(self.yc[:frame])
        return (self.line1, self.line2, self.line3, self.line4)
    

    # Pour changer les paramètre de commande et relancer le solver
    def update_simu(self, K, lc, ref_time, ampl, end_time):
        self.K = K
        self.lc = lc
        self.initial_amplitude = ampl
        self.start_reference_time = ref_time
        self.tspan = (0.0, end_time)
        self.t_eval = np.linspace(self.tspan[0], self.tspan[1], num=self.frame_count)
        self.ax.set(xlim=[0, self.tspan[1]], ylim=[min(-8,-self.initial_amplitude), max(8,self.initial_amplitude)], xlabel='Time [s]', ylabel='Amplitude')
        
        self.run_simulation()

    # Gestion de la mise en pause et recommencement (et fin d'animation)
    def toggle_pause(self, event):
        if event.key != ' ' and event.key != 'a': #Mettre pause que si on appuie sur espace et recommencer si on appuie sur a
            return
        elif event.key == ' ':
            if self.ani is None: #Pour la première itération
                self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=self.frame_count, interval=10, repeat=False)
                self.paused = False
                self.fig.canvas.draw()
            elif self.paused and self.simulation_end == False:
                self.ani.resume()
                self.paused = False
            elif self.simulation_end == False:
                self.ani.pause()
                self.paused = True
        else:
            if self.ani is not None and self.paused == True:
                # L'update de la simu ne doit être fait que lors su changement des sliders
                # Il faudrait que si les sliders sont changés on reprend comme avant
                # Et si on appuie sur une certaine touche, on recommence à zéro
                self.paused = False
                self.update_simu(self.K, self.lc, self.start_reference_time, self.initial_amplitude, self.tspan[1])
                self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=self.frame_count, interval=10, repeat=False)
                self.fig.canvas.draw()
                self.simulation_end = False

    def get_K(self):
        return self.K
    
    def get_lc(self):
        return self.lc


#anim = MyAnimation(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, 0, 1, 10)
#plt.show()