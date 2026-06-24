import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

import animation as ma

class Mainwindow:
    def __init__(self, root):
        self.root = root
        
        # Configuration de la fenêtre de simulation
        self.root.title("Simulations's interactive interface")
        self.root.geometry("400x300") # Légèrement élargi pour s'adapter aux polices Linux natives
        
        # Variables internes (initialisation identique)
        self.anim = None
        self.first_input = True
        self.reference = 0
        self.wn = 5.0
        self.z = 0.69
        self.tf = 3
        self.plot_type = 'Moving points'
        
        # --- main_layout (Equivalent QVBoxLayout) ---
        # Texte en haut, au milieu
        self.label = tk.Label(root, text="Configure your parameters below :")
        self.label.pack(pady=10)

        # --- slider_layout (Equivalent QHBoxLayout) ---
        slider_frame = tk.Frame(root)
        slider_frame.pack(pady=10, fill="x", padx=10)
        
        # Pour aligner les 4 blocs côte à côte proprement, on utilise .grid() dans le slider_frame
        # Configurer l'expansion des colonnes pour un espacement régulier
        for c in range(8):
            slider_frame.grid_columnconfigure(c, weight=1)

        # --- 1. Bloc yc ---
        self.yc_title = tk.Label(slider_frame, text="yc", font=("Arial", 10, "bold"))
        self.yc_title.grid(row=0, column=0, sticky="n")
        
        self.label_max_yc = tk.Label(slider_frame, text="30", fg="grey")
        self.label_max_yc.grid(row=1, column=0)
        
        # En Tkinter, un Scale vertical va du haut (valeur min) vers le bas (valeur max). 
        # Pour inverser et avoir le max en haut, on met from_=30 et to=-30
        self.slider_yc = tk.Scale(slider_frame, from_=30, to=-30, orient="vertical", length=150, command=self.value_changed_yc)
        self.slider_yc.set(0)
        self.slider_yc.grid(row=2, column=0, pady=5)
        
        self.label_min_yc = tk.Label(slider_frame, text="-30", fg="grey")
        self.label_min_yc.grid(row=3, column=0)
        
        self.label_yc_value = tk.Label(slider_frame, text="0", font=("Arial", 10, "bold"))
        self.label_yc_value.grid(row=2, column=1, padx=5)

        # --- 2. Bloc wn ---
        self.wn_title = tk.Label(slider_frame, text="wn", font=("Arial", 10, "bold"))
        self.wn_title.grid(row=0, column=2, sticky="n")
        
        self.label_max_wn = tk.Label(slider_frame, text="15", fg="grey")
        self.label_max_wn.grid(row=1, column=2)
        
        self.slider_wn = tk.Scale(slider_frame, from_=150, to=1, orient="vertical", length=150, command=self.value_changed_wn)
        self.slider_wn.set(50)
        self.slider_wn.grid(row=2, column=2, pady=5)
        
        self.label_min_wn = tk.Label(slider_frame, text="0", fg="grey")
        self.label_min_wn.grid(row=3, column=2)
        
        self.label_wn_value = tk.Label(slider_frame, text="5.0", font=("Arial", 10, "bold"))
        self.label_wn_value.grid(row=2, column=3, padx=5)

        # --- 3. Bloc z ---
        self.z_title = tk.Label(slider_frame, text="z", font=("Arial", 10, "bold"))
        self.z_title.grid(row=0, column=4, sticky="n")
        
        self.label_max_z = tk.Label(slider_frame, text="2.0", fg="grey")
        self.label_max_z.grid(row=1, column=4)
        
        self.slider_z = tk.Scale(slider_frame, from_=200, to=10, orient="vertical", length=150, command=self.value_changed_z)
        self.slider_z.set(69)
        self.slider_z.grid(row=2, column=4, pady=5)
        
        self.label_min_z = tk.Label(slider_frame, text="0.1", fg="grey")
        self.label_min_z.grid(row=3, column=4)
        
        self.label_z_value = tk.Label(slider_frame, text="0.69", font=("Arial", 10, "bold"))
        self.label_z_value.grid(row=2, column=5, padx=5)

        # --- 4. Bloc tf ---
        self.tf_title = tk.Label(slider_frame, text="tf", font=("Arial", 10, "bold"))
        self.tf_title.grid(row=0, column=6, sticky="n")
        
        self.label_max_tf = tk.Label(slider_frame, text="40", fg="grey")
        self.label_max_tf.grid(row=1, column=6)
        
        self.slider_tf = tk.Scale(slider_frame, from_=40, to=0, orient="vertical", length=150, command=self.value_changed_tf)
        self.slider_tf.set(3)
        self.slider_tf.grid(row=2, column=6, pady=5)
        
        self.label_min_tf = tk.Label(slider_frame, text="0", fg="grey")
        self.label_min_tf.grid(row=3, column=6)
        
        self.label_tf_value = tk.Label(slider_frame, text="3", font=("Arial", 10, "bold"))
        self.label_tf_value.grid(row=2, column=7, padx=5)


        # --- bottom_layout (Equivalent QHBoxLayout) ---
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=15, fill="x", padx=20)
        
        # Zone de texte gauche (Equivalent bottom_text_layout QVBoxLayout)
        bottom_text_frame = tk.Frame(bottom_frame)
        bottom_text_frame.pack(side="left")
        
        self.label3 = tk.Label(bottom_text_frame, text="Press spacebar : pause/play", font=("Arial", 9, "underline", "bold"))
        self.label3.pack(anchor="w")
        self.label4 = tk.Label(bottom_text_frame, text="Press 'a' : reset simulation", font=("Arial", 9, "underline", "bold"))
        self.label4.pack(anchor="w")
        
        # Combobox à droite (Equivalent QComboBox)
        self.box = ttk.Combobox(bottom_frame, values=['Moving points', 'Moving curves', 'Curve filling'], state="readonly")
        self.box.set('Moving points')
        self.box.bind("<<ComboboxSelected>>", self.value_changed_plot)
        self.box.pack(side="right", padx=5)
        
        self.label5 = tk.Label(bottom_frame, text="Plotting type :")
        self.label5.pack(side="right", padx=5)


        # --- Bouton et Zone de message (Mise à jour des paramètres) ---
        self.button = tk.Button(root, text="Start simulation", command=self.button_clicked, bg="#4C729F", fg="white", font=("Arial", 10, "bold"))
        self.button.pack(pady=10, ipadx=10, ipady=3)
        
        self.label2 = tk.Label(root, text="", fg="darkgreen")
        self.label2.pack()

        # Gestion de l'id de l'animation de fadeout de Tkinter
        self.fade_job = None

    def button_clicked(self):
        # Annulation du fadeout précédent s'il tourne encore
        if self.fade_job is not None:
            self.root.after_cancel(self.fade_job)
            self.fade_job = None
        
        # Réinitialisation de l'affichage de la couleur du texte (opacité 1.0)
        self.label2.config(fg="darkgreen")

        # Calcul exact de la logique métier
        (K, lc) = ma.compute_K_lc(self.wn, self.z)

        if not self.first_input:
            self.anim.update_simu(K, lc, self.reference, self.tf, self.plot_type)
            self.label2.config(text='Parameters have been updated, ready for next restart !!!')
        else:
            self.anim = ma.MyAnimation(K, lc, self.reference, self.tf, self.plot_type)
            self.button.config(text='Update inputs')
            self.label2.config(text='Simulation started !')
            self.first_input = False
            plt.show()
            
        # Lancement de l'animation de disparition du texte (Fading de 2000 ms)
        self.fade_out(2000)

    # Fonctions de changement de valeurs (Mêmes opérations mathématiques sur les sliders)
    def value_changed_yc(self, value):
        self.reference = int(value)
        self.label_yc_value.config(text=str(self.reference))

    def value_changed_wn(self, value):
        self.wn = float(value) / 10
        self.label_wn_value.config(text=f"{self.wn:.1f}")

    def value_changed_z(self, value):
        self.z = float(value) / 100
        self.label_z_value.config(text=f"{self.z:.2f}")

    def value_changed_tf(self, value):
        self.tf = int(value)
        self.label_tf_value.config(text=str(self.tf))

    def value_changed_plot(self, event):
        value = self.box.get()
        if value == 'Moving points':
            self.moving_points = True
        else:
            self.moving_points = False
        self.plot_type = value

    def fade_out(self, duration_ms):
        """Simule l'animation PySide6 de fading (QPropertyAnimation) en modifiant 
        la couleur du texte vers le blanc du fond de la fenêtre de façon itérative."""
        steps = 20
        delay = duration_ms // steps
        
        def run_fade(step=0):
            if step <= steps:
                # Calcul de la transition de couleur du vert foncé vers le gris/blanc de fond
                # Rapprochement progressif vers le gris par défaut de Tkinter (#f0f0f0 sous Windows/Linux standard)
                alpha = step / steps
                # On fait simplement disparaître le texte à la fin
                if step == steps:
                    self.label2.config(text="")
                else:
                    # Changement de couleur graduel pour mimer la transparence
                    gray_val = int(0 + (240 * alpha)) # Part de 0 (Noir/Vert) vers 240 (Gris clair)
                    hex_color = f"#{gray_val:02x}{200 if gray_val < 200 else gray_val:02x}{gray_val:02x}"
                    self.label2.config(fg=hex_color)
                    self.fade_job = self.root.after(delay, lambda: run_fade(step + 1))
        run_fade()

def main():
    root = tk.Tk()
    app = Mainwindow(root)
    root.mainloop() # Start application

if __name__ == "__main__":
    main()