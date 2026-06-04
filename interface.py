import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout

import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal, integrate
import math
from control import matlab

from scipy.integrate import solve_ivp

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My simulation')
        self.setGeometry(390, 150, 800, 500)

        layout = QVBoxLayout()

        self.button = QPushButton('Start simulation')
        self.label = QLabel('Informative text area')

        self.button.clicked.connect(self.button_clicked)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)


    def button_clicked(self):
        self.label.setText('The button was clicked')


def main():
    app = QApplication([])
    window = Mainwindow()
    window.show()
    sys.exit(app.exec()) #Start application

if __name__ == "__main__":
    main()