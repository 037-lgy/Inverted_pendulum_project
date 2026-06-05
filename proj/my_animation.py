import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import NXTwaysim as nxt
from scipy.integrate import solve_ivp
import math

def consigne_temp(t, start_time, amplitude):
    if t < start_time:
        return 0
    else:
        return amplitude

class MyAnimation:
    def __init__(self, K, lc, ref_time, ref_ampl):
        self.K = K
        self.lc = lc

        self.depassement = 0

        self.fig, self.ax = plt.subplots()

        self.tspan = (0.0, 2.0)
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
        self.ax.set(xlim=[0, 2], ylim=[-8, 8], xlabel='Time [s]', ylabel='Amplitude')
        self.ax.legend()

        # Commence par rien n'afficher
        self.paused = True
        
        # Pour permettre au premier déclenchement de se faire lors du premier appuie sur espace
        self.ani = None


        # Relier le fait de mettre sur pause et relancer avec espace
        #Il faudra relier l'appel de update simu au changement d'interface graphique
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_pause)

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
            self.ax.text(0, 9, f'Overshoot : {round(depassement,1)} %')
            self.paused = True
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
    def update_simu(self, K, lc, time, ampl):
        self.K = K
        self.lc = lc
        self.initial_amplitude = ampl
        self.start_reference_time = time
        
        self.run_simulation()

    # Gestion de la mise en pause (et fin d'animation)
    def toggle_pause(self, event):
        if event.key != ' ': #Mettre pause que si on appuie sur espace
            return
        if self.ani is None: #Pour la première itération
            self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=self.frame_count, interval=10, repeat=False)
            self.paused = False
            self.fig.canvas.draw()
        elif self.paused: 
            # L'update de la simu ne doit être fait que lors su changement des sliders
            # Il faudrait que si les sliders sont changés on reprend comme avant
            # Et si on appuie sur une certaine touche, on recommence à zéro
            self.update_simu(self.K, self.lc, self.start_reference_time, self.initial_amplitude)
            self.ani = animation.FuncAnimation(fig=self.fig, func=self.update, frames=self.frame_count, interval=10, repeat=False)
            self.ani.resume()
            self.paused = False
            self.fig.canvas.draw()
        else:
            self.ani.pause()
            self.paused = True

#anim = MyAnimation(np.array([[-5.5148, -34.12178, -1.7862, -2.8974]]), -5.5148, consigne_temp, 0, 1)
#plt.show()