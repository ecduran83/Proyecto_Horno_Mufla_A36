from PySide6.QtWidgets import QDialog
from app.ui.ui_constantes_pid import Ui_Dialog
from app.controllers.furnace_operations import FurnaceOperations
from app.models.calculo_datos import CalculosDatos

class PidConstants(QDialog, Ui_Dialog):

    def __init__(self, calculos:CalculosDatos):
        super().__init__()
        self.setupUi(self)
        self.calculos = calculos

    def send_const(self, fo:FurnaceOperations):
        kp = self.spin_kp.value()
        ki = self.spin_ki.value()
        kd = self.spin_kd.value()
        self._change_constants_in_gui(kp, ki, kd)
        fo.send_constants_pid([kp, ki, kd])

    def _change_constants_in_gui(self, kp, ki, kd):
        self.calculos.Kp = kp
        self.calculos.Ki = ki
        self.calculos.Kd = kd

