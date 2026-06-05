import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout

import NXTwaysim as nxt
import BE_script as be

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulations's interface")
        self.setGeometry(390, 150, 800, 500)

        layout = QVBoxLayout()

        self.button = QPushButton('Start simulation')
        self.label1 = QLabel('K :')
        self.label2 = QLabel('lc :')

        self.button.clicked.connect(self.button_clicked)

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)


    def button_clicked(self):
        self.label1.setText('The button was clicked')


def main():
    app = QApplication([])
    window = Mainwindow()
    window.show()
    sys.exit(app.exec()) #Start application

if __name__ == "__main__":
    main()