import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation
import matplotlib.pyplot as plt

import my_animation as ma

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulations's interactive interface")
        self.setGeometry(0, 150, 450, 350)

        main_layout = QVBoxLayout()

        self.label = QLabel("Configure your parameters below :")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.label)



        slider_layout = QHBoxLayout()

        yc_block = QVBoxLayout()

        self.yc_title = QLabel('<b>yc<b>')
        self.yc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_max_yc = QLabel('10')
        self.label_max_yc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_yc = QSlider(Qt.Orientation.Vertical)
        self.slider_yc.setRange(-10, 10)
        self.slider_yc.setValue(0)
        self.slider_yc.valueChanged.connect(self.value_changed_yc)
        self.slider_yc.setTickPosition(QSlider.TickPosition.TicksLeft)

        self.label_min_yc = QLabel('-10')
        self.label_min_yc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yc_block.addWidget(self.yc_title)
        yc_block.addWidget(self.label_max_yc)
        yc_block.addWidget(self.slider_yc, alignment=Qt.AlignmentFlag.AlignHCenter)
        yc_block.addWidget(self.label_min_yc)

        slider_layout.addLayout(yc_block)

        self.label_yc_value = QLabel('0')
        self.label_yc_value.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        slider_layout.addWidget(self.label_yc_value)

        wn_block = QVBoxLayout()

        self.wn_title = QLabel('<b>wn<b>')
        self.wn_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_max_wn = QLabel('15')
        self.label_max_wn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_wn = QSlider(Qt.Orientation.Vertical)
        self.slider_wn.setRange(1, 150)
        self.slider_wn.setValue(50)
        self.slider_wn.valueChanged.connect(self.value_changed_wn)
        self.slider_wn.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider_wn.setTickInterval(10)

        self.label_min_wn = QLabel('0')
        self.label_min_wn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wn_block.addWidget(self.wn_title)
        wn_block.addWidget(self.label_max_wn)
        wn_block.addWidget(self.slider_wn, alignment=Qt.AlignmentFlag.AlignHCenter)
        wn_block.addWidget(self.label_min_wn)

        slider_layout.addLayout(wn_block)

        self.label_wn_value = QLabel('5.0')
        self.label_wn_value.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        slider_layout.addWidget(self.label_wn_value)


        z_block = QVBoxLayout()

        self.z_title = QLabel('<b>z<b>')
        self.z_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_max_z = QLabel('1.0')
        self.label_max_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_z = QSlider(Qt.Orientation.Vertical)
        self.slider_z.setRange(0, 100)
        self.slider_z.setValue(69)
        self.slider_z.valueChanged.connect(self.value_changed_z)
        self.slider_z.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider_z.setTickInterval(10)

        self.label_min_z = QLabel('0.0')
        self.label_min_z.setAlignment(Qt.AlignmentFlag.AlignCenter)


        z_block.addWidget(self.z_title)
        z_block.addWidget(self.label_max_z)
        z_block.addWidget(self.slider_z, alignment=Qt.AlignmentFlag.AlignHCenter)
        z_block.addWidget(self.label_min_z)

        slider_layout.addLayout(z_block)

        self.label_z_value = QLabel('0.69')
        self.label_z_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout.addWidget(self.label_z_value)

        tf_block = QVBoxLayout()

        self.tf_title = QLabel('<b>tf<b>')
        self.tf_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_max_tf = QLabel('40')
        self.label_max_tf.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_tf = QSlider(Qt.Orientation.Vertical)
        self.slider_tf.setRange(0, 40)
        self.slider_tf.setValue(5)
        self.slider_tf.valueChanged.connect(self.value_changed_tf)
        self.slider_tf.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider_tf.setTickInterval(5)

        self.label_min_tf = QLabel('0')
        self.label_min_tf.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tf_block.addWidget(self.tf_title)
        tf_block.addWidget(self.label_max_tf)
        tf_block.addWidget(self.slider_tf, alignment=Qt.AlignmentFlag.AlignHCenter)
        tf_block.addWidget(self.label_min_tf)

        slider_layout.addLayout(tf_block)

        self.label_tf_value = QLabel('0')
        self.label_tf_value.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        slider_layout.addWidget(self.label_tf_value)

        main_layout.addLayout(slider_layout)

        self.button = QPushButton('Start simulation')
        self.button.clicked.connect(self.button_clicked)

        self.label2 = QLabel()
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.opacity_effect = QGraphicsOpacityEffect(self.label2)
        self.label2.setGraphicsEffect(self.opacity_effect)

        self.label3 = QLabel('<b><u>Press spacebar : pause/play<b><u>')
        self.label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label4 = QLabel("<b><u>Press 'a' : restart simulation<b><u>")
        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Animation pour faire disparaitre le texte de mise à jour des paramètres
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)


        main_layout.addWidget(self.label3)
        main_layout.addWidget(self.label4)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.label2)

        window = QWidget()
        window.setLayout(main_layout)

        self.setCentralWidget(window)

        self.anim = None
        self.first_input = True
        self.reference = 0
        self.wn = 5.0
        self.z = 0.69
        self.tf = 5


    def button_clicked(self):
        self.fade_animation.stop()
        self.opacity_effect.setOpacity(1.0)

        (K, lc) = ma.compute_K_lc(self.wn, self.z)

        if not self.first_input:
            self.anim.update_simu(K, lc, 0, self.reference, self.tf)
            self.label2.setText('Parameters have been updated, ready for next restart !!!')
        else:
            self.anim = ma.MyAnimation(K, lc, 0, self.reference, self.tf)
            self.button.setText('Update inputs')
            self.label2.setText('Simulation started !')
            self.first_input = False
            plt.show()
        self.fade_animation.start()

    def value_changed_yc(self, value):
        self.reference = value
        self.label_yc_value.setText(str(self.reference))

    def value_changed_wn(self, value):
        self.wn = value/10
        self.label_wn_value.setText(str(self.wn))

    def value_changed_z(self, value):
        self.z = value/100
        self.label_z_value.setText(str(self.z))

    def value_changed_tf(self, value):
        self.tf = value
        self.label_tf_value.setText(str(self.tf))


def main():
    app = QApplication([])
    window = Mainwindow()
    window.show()
    sys.exit(app.exec()) #Start application

if __name__ == "__main__":
    main()