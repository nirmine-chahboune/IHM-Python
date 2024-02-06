import sys  # Importez le module sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont

import subprocess

class InterfaceOpener(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestion Stock")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        button_font = QFont("Arial", 12)

        button_1 = QPushButton("Gestion Client", self)
        button_1.setFont(button_font)
        button_1.clicked.connect(self.open_interface_1)
        layout.addWidget(button_1)

        button_2 = QPushButton("Gestion Commande", self)
        button_2.setFont(button_font)
        button_2.clicked.connect(self.open_interface_2)
        layout.addWidget(button_2)



        button_3 = QPushButton("Gestion Produit", self)
        button_3.setFont(button_font)
        button_3.clicked.connect(self.perform_action_3)
        layout.addWidget(button_3)

        self.setLayout(layout)

    def open_interface_1(self):
        subprocess.Popen(["python", "GestionClient.py"])

    def open_interface_2(self):
        subprocess.Popen(["python", "GestionCommande.py"])



    def perform_action_3(self):
        subprocess.Popen(["python", "GestionProduit.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceOpener()
    window.show()
    sys.exit(app.exec_())

