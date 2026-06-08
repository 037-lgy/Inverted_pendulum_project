import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

import my_animation as ma

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulations's interactive interface")
        self.setGeometry(50, 150, 400, 200)

        main_layout = QVBoxLayout()

        self.label = QLabel("Configure your parameters below :")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.label)



        slider_layout = QHBoxLayout()

        yc_block = QVBoxLayout()

        self.yc_title = QLabel('yc reference')
        self.yc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_yc = QSlider(Qt.Orientation.Vertical)
        self.slider_yc.setRange(-10, 10)
        self.slider_yc.setValue(0)
        self.slider_yc.valueChanged.connect(self.value_changed_yc)
        self.slider_yc.sliderReleased.connect(self.update_reference)

        self.label_yc_value = QLabel('0')
        self.label_yc_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yc_block.addWidget(self.yc_title)
        yc_block.addWidget(self.slider_yc, alignment=Qt.AlignmentFlag.AlignHCenter)
        yc_block.addWidget(self.label_yc_value)

        slider_layout.addLayout(yc_block)       


        wn_block = QVBoxLayout()

        self.wn_title = QLabel('wn')
        self.wn_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_wn = QSlider(Qt.Orientation.Vertical)
        self.slider_wn.setRange(1, 150)
        self.slider_wn.setValue(50)
        self.slider_wn.valueChanged.connect(self.value_changed_wn)
        self.slider_wn.sliderReleased.connect(self.update_wn)

        self.label_wn_value = QLabel('5.0')
        self.label_wn_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wn_block.addWidget(self.wn_title)
        wn_block.addWidget(self.slider_wn, alignment=Qt.AlignmentFlag.AlignHCenter)
        wn_block.addWidget(self.label_wn_value)

        slider_layout.addLayout(wn_block)


        z_block = QVBoxLayout()

        self.z_title = QLabel('z')
        self.z_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_z = QSlider(Qt.Orientation.Vertical)
        self.slider_z.setRange(0, 100)
        self.slider_z.setValue(69)
        self.slider_z.valueChanged.connect(self.value_changed_z)
        self.slider_z.sliderReleased.connect(self.update_z)

        self.label_z_value = QLabel('0.69')
        self.label_z_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        z_block.addWidget(self.z_title)
        z_block.addWidget(self.slider_z, alignment=Qt.AlignmentFlag.AlignHCenter)
        z_block.addWidget(self.label_z_value)

        slider_layout.addLayout(z_block)

        main_layout.addLayout(slider_layout)

        self.button = QPushButton('Start simulation')
        self.button.clicked.connect(self.button_clicked)
        main_layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(main_layout)

        self.setCentralWidget(window)

        self.anim = None
        self.first_input = True
        self.reference = 0
        self.wn = 5.0
        self.z = 0.69


    def button_clicked(self):
        (K, lc) = ma.compute_K_lc(self.wn, self.z)
        if not self.first_input:
            self.anim.update_simu(K, lc, 0, self.reference, int(4/self.wn) + 3)
        else:
            self.anim = ma.MyAnimation(K, lc, 0, self.reference, int(4/self.wn) + 3)
            self.button.setText('Update inputs')
            self.first_input = False

    def value_changed_yc(self, value):
        self.reference = value
        self.label_yc_value.setText(str(self.reference))

    def value_changed_wn(self, value):
        self.wn = value/10
        self.label_wn_value.setText(str(self.wn))

    def value_changed_z(self, value):
        self.z = value/100
        self.label_z_value.setText(str(self.z))


    def update_reference(self):
        print(self.reference)

    def update_wn(self):
        print(self.wn)

    def update_z(self):
        print(self.z)


def main():
    app = QApplication([])
    window = Mainwindow()
    window.show()
    sys.exit(app.exec()) #Start application

if __name__ == "__main__":
    main()