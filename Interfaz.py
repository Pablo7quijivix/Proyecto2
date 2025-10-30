print(f"Agregando archivo adicional en donde se alojara la parte grafica")

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QLabel, QHBoxLayout)
from Proyecto_2 import Auditor, Usuario  # Importamos la lógica

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Funciones de Auditor")

        self.logica_auditor= Auditor(Usuario)

        self.inicializar_ui()
print(f"actualizacion de la interfaz grafica con herramientas de Qt Designer")