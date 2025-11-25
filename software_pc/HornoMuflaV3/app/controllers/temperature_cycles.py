from PySide6.QtWidgets import QDialog
from app.ui.ui_programacion_ciclos import Ui_Dialog
from app.controllers.json_manager import JsonManager
import json
import sys
import os

class TemperatureCycles(QDialog, Ui_Dialog):

    def __init__(self, jm:JsonManager):
        super().__init__()
        self.setupUi(self)
        self.jm = jm
        self.cargar_perfiles()

        # Condiciones iniciales de las opciones de la ventana
        self.spin_masa.setEnabled(False)
        self.combo_material.setEnabled(False)
        self.spin_velocidad.setEnabled(False)

        # Señales de la ventana de ciclos
        self.check_masa.stateChanged.connect(self.check_masa_fn)
        self.check_velocidad.stateChanged.connect(self.check_velocidad_fn)

    def check_masa_fn(self):
        if self.check_masa.isChecked():
            self.combo_material.setEnabled(True)
            self.spin_masa.setEnabled(True)
        else:
            self.combo_material.setEnabled(False)
            self.spin_masa.setEnabled(False)

    def check_velocidad_fn(self):
        if self.check_velocidad.isChecked():
            self.spin_velocidad.setEnabled(True)
        else:
            self.spin_velocidad.setEnabled(False)

    def cargar_perfiles(self):
        self.combo_material.clear()
        materiales = self.jm.cargar_perfiles_json()
        self.combo_material.addItems(materiales)







