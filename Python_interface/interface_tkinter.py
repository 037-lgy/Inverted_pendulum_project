import tkinter as tk
import matplotlib.pyplot as plt

import animation as ma

class Mainwindow:
    def __init__(self, root):
        self.root = root
        
        # Configuration de la fenêtre de simulation
        self.root.title("Simulations's interactive interface")
        self.root.geometry("500x400")
        
        # Création de l'animation
        self.anim = None

        # Variable pour le tout début de la simulation
        self.first_input = True

        # Référence initiale du slider yc
        self.reference = 0

        # Référence initiale du slider wn
        self.wn = 5.0

        # Référence initiale du slider z
        self.z = 0.69

        # Référence initiale du slider tf
        self.tf = 3

        # Premier texte en haut, au milieu
        self.label = tk.Label(root, text="Configure your parameters below :")
        self.label.pack(pady=10)

        # Layout pour les slider alignés horizontalement
        slider_frame = tk.Frame(root)
        slider_frame.pack(pady=10, fill="x", padx=10)
        
        # Pour aligner les 4 blocs côte à côte proprement, on utilise .grid() dans le slider_frame, avec 8 colonnes
        for c in range(8):
            slider_frame.grid_columnconfigure(c, weight=1)

        # Bloc yc ------------------------------------------------------------------------

        # Nom du slider
        self.yc_title = tk.Label(slider_frame, text="yc", font=("Arial", 10, "bold"))
        self.yc_title.grid(row=0, column=0, sticky="n")
        
        # Valeur max du slider
        self.label_max_yc = tk.Label(slider_frame, text="30", fg="grey")
        self.label_max_yc.grid(row=1, column=0)
        
        # Slider
        self.slider_yc = tk.Scale(slider_frame, from_=30, to=-30, orient="vertical", length=150, command=self.value_changed_yc)
        self.slider_yc.set(0)
        self.slider_yc.grid(row=2, column=0, pady=5)
        
        # Valeur min du slideur
        self.label_min_yc = tk.Label(slider_frame, text="-30", fg="grey")
        self.label_min_yc.grid(row=3, column=0)
        
        # Valeur actuelle du slideur
        self.label_yc_value = tk.Label(slider_frame, text="0", font=("Arial", 10, "bold"))
        self.label_yc_value.grid(row=2, column=1, padx=5)

        # Bloc wn -----------------------------------------------------------------------


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

        # Bloc z ------------------------------------------------------------------------


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

        # Bloc tspan --------------------------------------------------------------------


        self.tf_title = tk.Label(slider_frame, text="tspan", font=("Arial", 10, "bold"))
        self.tf_title.grid(row=0, column=6, sticky="n")
        
        self.label_max_tf = tk.Label(slider_frame, text="40", fg="grey")
        self.label_max_tf.grid(row=1, column=6)
        
        self.slider_tf = tk.Scale(slider_frame, from_=40, to=2, orient="vertical", length=150, command=self.value_changed_tf)
        self.slider_tf.set(3)
        self.slider_tf.grid(row=2, column=6, pady=5)
        
        self.label_min_tf = tk.Label(slider_frame, text="0", fg="grey")
        self.label_min_tf.grid(row=3, column=6)
        
        self.label_tf_value = tk.Label(slider_frame, text="3", font=("Arial", 10, "bold"))
        self.label_tf_value.grid(row=2, column=7, padx=5)


        # Zone du bas  -----------------------------------------------------------------
        
        self.label3 = tk.Label(root, text="Press spacebar : pause/play", font=("Arial", 10, "underline", "bold"))
        self.label3.pack(pady=1)
        self.label4 = tk.Label(root, text="Press 'a' : reset simulation", font=("Arial", 10, "underline", "bold"))
        self.label4.pack(pady=1)

        # Bouton de lancement et d'update de la simulation
        self.button = tk.Button(root, text="Start simulation", command=self.button_clicked, bg="#4C729F", fg="white", font=("Arial", 10, "bold"))
        self.button.pack(pady=10, ipadx=10, ipady=3)

    # Fonction appelée quand on appuie sur le bouton
    def button_clicked(self):

        (K, lc) = ma.compute_K_lc(self.wn, self.z)

        if not self.first_input:
            self.anim.update_simu(K, lc, self.reference, self.tf)
        else:
            self.anim = ma.MyAnimation(K, lc, self.reference, self.tf)
            self.button.config(text='Update inputs')
            self.first_input = False
            plt.show()

    # Fonctions de changement des valeurs des sliders
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

def main():
    root = tk.Tk()
    app = Mainwindow(root)
    root.mainloop() # Start application

if __name__ == "__main__":
    main()