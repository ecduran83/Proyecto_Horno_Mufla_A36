from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt, QIcon

from app.ui.ui_main_window import Ui_MainWindow
from app.controllers.serial_operations import SerialOperations
from app.controllers.heart_beat import HeartBeat
from app.controllers.furnace_operations import FurnaceOperations
from app.models.graphing_tool import GraphingTool
from app.controllers.perfil_manager import PerfilManager
from app.controllers.temperature_cycles import TemperatureCycles
from app.controllers.pid_constants import PidConstants
from app.controllers.add_materials import AddMaterials
from app.controllers.add_materials import JsonManager

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QSplashScreen
import time
import sys
import os

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Instancias de tareas en paralelos
        self.serial_op = SerialOperations()
        self.jm = JsonManager()
        self.hb = HeartBeat(self.serial_op)
        self.fo = FurnaceOperations(self.serial_op)
        self.gt = GraphingTool(self.grafica)
        self.pm = PerfilManager(self.serial_op, self.tab_agregarPerfil, self.gt, self.jm)

        # Instancias de otras ventanas
        self.ciclos = TemperatureCycles(self.jm)
        self.constantes_pid = PidConstants(self.gt.calculo)
        self.agreg_mat = AddMaterials(self.jm)

        # Señales que envían desde otras clases
        self.serial_op.device_not_found_in_list_port.connect(self.device_not_found_fn)
        self.serial_op.device_connected.connect(self.device_connected_fn)
        self.serial_op.device_unconnected.connect(self.device_unconnected_fn)
        self.serial_op.temp_received.connect(self.temp_received_fn)
        self.serial_op.lost_connection.connect(self.lost_connection_fn)
        self.serial_op.resp_set_controller.connect(self.resp_set_controller_fn)
        self.serial_op.power_value.connect(self.power_value_fn)
        self.serial_op.temp_with_process.connect(self.temp_with_process_fn)
        self.pm.signal_profile.connect(self.signal_profile_fn)
        self.jm.signal_json_err.connect(self.signal_json_err_fn)
        self.jm.signal_json_save.connect(self.signal_json_save_fn)

        # Señales enviadas desde la GUI
        self.btn_conectar.clicked.connect(self.btn_conectar_fn)
        self.btn_enviarSetpoint.clicked.connect(self.btn_enviar_setpoint_fn)
        self.btn_iniciarSetpoint.clicked.connect(self.btn_iniciar_setpoint_fn)
        self.btn_agregar_etapa.clicked.connect(self.btn_agregar_etapa_fn)
        self.btn_eliminar_etapa.clicked.connect(self.btn_eliminar_etapa_fn)
        self.btn_eliminar_perfil.clicked.connect(self.btn_eliminar_perfil_fn)
        self.btn_enviarPerfil.clicked.connect(self.btn_enviar_perfil_fn)
        self.btn_iniciarPerfil.clicked.connect(self.btn_iniciar_perfil_fn)
        self.btn_enviarPotenciaFija.clicked.connect(self.btn_enviar_potencia_fija_fn)
        self.btn_iniciarPotenciaFija.clicked.connect(self.btn_iniciar_potencia_fija_fn)
        self.action_ajustarPID.triggered.connect(self.constantes_pid_fn)
        self.actionAgregar_Material.triggered.connect(self.agregar_material)
        self.agreg_mat.btn_agregarMaterial.clicked.connect(self.btn_agregar_material_fn)
        self.agreg_mat.btn_eliminarMaterial.clicked.connect(self.btn_eliminar_material_fn)

        self.disable_buttons()


    def btn_conectar_fn(self):
        if not self.serial_op.device_ok:
            self.serial_op.validate_device()
        else:
            self.serial_op.disconnect_device()
            self.disable_buttons()

    def device_connected_fn(self, message):
        self.log_consola.appendPlainText(message)
        self.label.setStyleSheet('color:green')
        self.label.setText('Conectado')
        self.btn_conectar.setText('Desconectar')
        self.hb.start_heart_beat()
        self.enable_buttons()

    def enable_buttons(self):
        self.btn_enviarSetpoint.setEnabled(True)
        self.btn_iniciarSetpoint.setEnabled(True)
        self.btn_enviarPerfil.setEnabled(True)
        self.btn_iniciarPerfil.setEnabled(True)
        self.btn_enviarPotenciaFija.setEnabled(True)
        self.btn_iniciarPotenciaFija.setEnabled(True)
        self.constantes_pid.setEnabled(True)

    def disable_buttons(self):
        self.btn_enviarSetpoint.setEnabled(False)
        self.btn_iniciarSetpoint.setEnabled(False)
        self.btn_enviarPerfil.setEnabled(False)
        self.btn_iniciarPerfil.setEnabled(False)
        self.btn_enviarPotenciaFija.setEnabled(False)
        self.btn_iniciarPotenciaFija.setEnabled(False)
        self.constantes_pid.setEnabled(False)
        self.bar_potenciaSetpoint.setValue(0)
        self.bar_potenciaPerfil.setValue(0)
        self.bar_potenciaFija.setValue(0)

    def device_not_found_fn(self, message):
        self.log_consola.appendPlainText(message)

    def device_unconnected_fn(self, message):
        self.log_consola.appendPlainText(message)
        self.label.setStyleSheet('colo:black')
        self.label.setText('Desconectado')
        self.btn_conectar.setText('Conectar')
        self.hb.stop_heart_beat()

    def temp_received_fn(self, temp):
        self.lcd_tempActual.display(temp)

    def lost_connection_fn(self):
        self.hb.stop_heart_beat()
        QMessageBox.critical(self, "Error", "Se ha perdido conexion con el horno.")
        self.label.setStyleSheet('colo:black')
        self.label.setText('Desconectado')
        self.btn_conectar.setText('Conectar')
        self.btn_conectar_fn()
        self.off_buttons()

    def btn_enviar_setpoint_fn(self):
        sp = self.spin_setpoint.value()
        self.gt.graficar_setpoint(sp, self.lcd_tempActual.value())
        self.lcd_setpoint.display(sp)
        self.fo.send_setpoint(sp)

    def resp_set_controller_fn(self, message):
        self.log_consola.appendPlainText(message)

    def power_value_fn(self, val):
        self.bar_potenciaSetpoint.setValue(val)
        self.bar_potenciaPerfil.setValue(val)
        self.bar_potenciaFija.setValue(val)

    def btn_iniciar_setpoint_fn(self):
        if not self.fo.is_running:
            self.btn_iniciarSetpoint.setText("Detener")
            self.btn_iniciarSetpoint.setStyleSheet("background-color: red; color: white;")
            self.fo.start_process()
            self.tab_rampaMeseta.setEnabled(False)
            self.tab.setEnabled(False)
        else:
            self.btn_iniciarSetpoint.setText("Comenzar")
            self.btn_iniciarSetpoint.setStyleSheet("")
            self.fo.stop_process()
            self.tab_rampaMeseta.setEnabled(True)
            self.tab.setEnabled(True)
            self.bar_in_zero()

    def temp_with_process_fn(self, temp):
        self.gt.graficar_real_time(temp)
        self.lcd_tempActual.display(temp)

    def btn_agregar_etapa_fn(self):
        self.ciclos.check_masa.setChecked(False)

        if self.tab_agregarPerfil.rowCount() > 0:
            self.ciclos.check_masa.setEnabled(False)
        else:
            self.ciclos.check_masa.setEnabled(True)

        self.ciclos.spin_masa.clear()
        self.ciclos.spin_velocidad.clear()
        self.ciclos.spin_tiempo_meseta.clear()
        self.ciclos.spin_temp_objetivo.clear()
        resp = self.ciclos.exec()

        if resp == QDialog.DialogCode.Accepted:
            speed = self.ciclos.spin_velocidad.value()
            setpoint = self.ciclos.spin_temp_objetivo.value()
            meseta = self.ciclos.spin_tiempo_meseta.value()
            masa = self.ciclos.spin_masa.value()
            material = self.ciclos.combo_material.currentText()
            dates = f'{speed},{setpoint},{meseta},{masa},{material}'
            self.pm.add_stage(dates)

    def btn_eliminar_etapa_fn(self):
        current_row = self.tab_agregarPerfil.currentRow()
        self.pm.delete_stage(current_row, self.ciclos)

    def signal_profile_fn(self, message):
        self.log_consola.appendPlainText(message)
        if '[END]' in message:
            pass

    def btn_eliminar_perfil_fn(self):
        self.pm.delete_profile(self.ciclos)

    def btn_enviar_perfil_fn(self):
        t_amb = self.lcd_tempActual.value()
        self.pm.graphic_perfil(t_amb)
        self.pm.send_command_profile()

    def btn_iniciar_perfil_fn(self):
        if not self.fo.is_running:
            self.btn_iniciarPerfil.setText("Detener")
            self.btn_iniciarPerfil.setStyleSheet("background-color: red; color: white;")
            self.fo.start_process()
            self.tab_setpoint.setEnabled(False)
            self.tab.setEnabled(False)
        else:
            self.btn_iniciarPerfil.setText("Comenzar")
            self.btn_iniciarPerfil.setStyleSheet("")
            self.fo.stop_process()
            self.tab_setpoint.setEnabled(True)
            self.tab.setEnabled(True)
            self.bar_in_zero()

    def bar_in_zero(self):
        self.bar_potenciaSetpoint.setValue(0)
        self.bar_potenciaPerfil.setValue(0)
        self.bar_potenciaFija.setValue(0)

    def off_buttons(self):
        self.fo.stop_process()
        self.btn_iniciarPerfil.setText("Comenzar")
        self.btn_iniciarPerfil.setStyleSheet("")
        self.btn_iniciarSetpoint.setText("Comenzar")
        self.btn_iniciarSetpoint.setStyleSheet("")
        self.tab_setpoint.setEnabled(True)
        self.tab.setEnabled(True)
        self.tab_rampaMeseta.setEnabled(True)
        self.bar_potenciaSetpoint.setValue(0)
        self.bar_potenciaPerfil.setValue(0)
        self.bar_potenciaFija.setValue(0)
        self.log_consola.appendPlainText('[GUI] Conexión perdida')

    def btn_enviar_potencia_fija_fn(self):
        power = self.spin_potenciaFija.value()
        self.lcd_setpoint.display(0)
        self.fo.send_fix_power(power)
        self.gt.fix_grafic()

    def btn_iniciar_potencia_fija_fn(self):
        if not self.fo.is_running:
            self.btn_iniciarPotenciaFija.setText("Detener")
            self.btn_iniciarPotenciaFija.setStyleSheet("background-color: red; color: white;")
            self.fo.start_process()
            self.tab_setpoint.setEnabled(False)
            self.tab_rampaMeseta.setEnabled(False)
        else:
            self.btn_iniciarPotenciaFija.setText("Comenzar")
            self.btn_iniciarPotenciaFija.setStyleSheet("")
            self.fo.stop_process()
            self.tab_setpoint.setEnabled(True)
            self.tab_rampaMeseta.setEnabled(True)
            self.bar_in_zero()

    def constantes_pid_fn(self):
        self.constantes_pid.spin_kp.clear()
        self.constantes_pid.spin_ki.clear()
        self.constantes_pid.spin_kd.clear()

        resp = self.constantes_pid.exec()
        if resp == QDialog.DialogCode.Accepted:
            self.constantes_pid.send_const(self.fo)

    def agregar_material(self):
        self.agreg_mat.llenar_tabla()
        resp = self.agreg_mat.exec()
        if resp:
            self.agreg_mat.guardar_material_json()

    def btn_agregar_material_fn(self):
        self.agreg_mat.add_material.line_nombreMaterial.clear()
        self.agreg_mat.add_material.spin_densidad.clear()
        self.agreg_mat.add_material.spin_calorEsp.clear()
        self.agreg_mat.add_material.spin_emis.clear()
        resp = self.agreg_mat.d1.exec()
        if resp:
            self.agreg_mat.material_extra()

    def btn_eliminar_material_fn(self):
        self.agreg_mat.borrar_material()

    def signal_json_err_fn(self, message):
        self.log_consola.appendPlainText(message)

    def signal_json_save_fn(self):
        self.ciclos.cargar_perfiles()


def actualizar_carga(mensaje, progreso):
    # Muestra un texto sobre la imagen (Color blanco, alineación inferior)
    splash.showMessage(f"{mensaje}...", Qt.AlignmentFlag.AlignBottom |
                       Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    # Mantiene la GUI viva mientras "cargamos"
    app.processEvents()
    # Simula tiempo de trabajo
    time.sleep(0.5)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Si falla, estamos en modo de desarrollo (script normal)
        base_path = os.path.abspath(".")
    print(os.path.join(base_path, relative_path))

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    imagen_splash = QPixmap(resource_path('assets/horno_inicio.PNG'))
    nuevo_tamano = QSize(600, 400)
    imagen_redimensionada = imagen_splash.scaled(
        nuevo_tamano,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )
    splash = QSplashScreen(imagen_redimensionada)
    splash.show()
    actualizar_carga("Cargando configuración", 25)
    actualizar_carga("Verificando puertos COM", 50)
    actualizar_carga("Iniciando motor gráfico", 75)
    actualizar_carga("Listo", 100)
    app.setWindowIcon(QIcon(resource_path('assets/icono_horno.ico')))
    window = MainWindow()
    window.show()
    splash.finish(window)
    app.exec()