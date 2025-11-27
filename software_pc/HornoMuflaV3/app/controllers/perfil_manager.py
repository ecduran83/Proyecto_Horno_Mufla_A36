from app.controllers.serial_operations import SerialOperations
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Signal, QObject
from app.controllers.json_manager import JsonManager
from app.models.graphing_tool import GraphingTool
from app.controllers.temperature_cycles import TemperatureCycles
from app.ui.ui_main_window import Ui_MainWindow

class PerfilManager(QObject):

    signal_profile = Signal(str)

    def __init__(self, ser_op:SerialOperations, table:QTableWidget, gt:GraphingTool, jm:JsonManager):
        super().__init__()
        self.jm = jm
        self.gt = gt
        self._ser_op = ser_op
        self.table = table
        self._etapa = 0
        self._index_process = 0
        self._commands = []

        self._ser_op.signal_end_stage.connect(self.send_command_profile)

    def graphic_perfil(self, temp_amb):
        if self.table.rowCount() > 0:
            total_dates = self.extract_dates_table()
            profile = self.process_profile_dates(total_dates)
            material = self.get_properties_material(total_dates)
            masa = self.get_mass_material(total_dates)
            self.gt.graficar_perfil(profile, material, masa, temp_amb)
        else:
            self.signal_profile.emit('[GUI] No se definió ningún perfil.')

    def add_stage(self, stage:str):
        index = self.table.rowCount()
        self.table.insertRow(index)
        stage_list = stage.split(',')
        for col in range(len(stage_list)):
            self.table.setItem(index, col, QTableWidgetItem(stage_list[col]))
            
    def delete_stage(self, current:int, dialog:TemperatureCycles):
        if current < 0:
            self.signal_profile.emit('[GUI] Seleccione una fila.')
        else:
            self.table.removeRow(current)
            self.signal_profile.emit('[GUI] Fila seleccionada eliminada')
            print(self.table.currentRow())
        self.clear_dialog_window(dialog)

    def delete_profile(self, dialog:TemperatureCycles):
        if self.table.rowCount() > 0:
            self.table.setRowCount(0)
            self.signal_profile.emit('[GUI] Perfil completo eliminado')
        else:
            self.signal_profile.emit('[GUI] No se tiene ningún perfil definido')
        self.clear_dialog_window(dialog)


    def process_profile_dates(self, stages):
        thermal_profile = []
        for stage in stages:
            stage_current = {}
            if stage[0] == '0':
                stage_current['tipo'] = 'normal'
                stage_current['temp_obj_C'] = int(stage[1])
                thermal_profile.append(stage_current)
            else:
                stage_current['tipo'] = 'rampa'
                stage_current['temp_obj_C'] = int(stage[1])
                stage_current['tasa_C_min'] = int(stage[0])
                thermal_profile.append(stage_current)

            stage_current = {}
            if stage[2] != '0':
                stage_current['tipo'] = 'meseta'
                stage_current['duracion_min'] = int(stage[2])
                thermal_profile.append(stage_current)
        return thermal_profile

    def get_properties_material(self, total_dates):
        materiales = self.jm.cargar_json()
        material = total_dates[0][4]
        rho = materiales[material]['rho']
        cp = materiales[material]['cp']
        e = materiales[material]['e']
        return [rho, cp, e]

    def get_mass_material(self, total_dates):
        mass = 0.001
        if total_dates[0][3] != '0.0':
            mass = float(total_dates[0][3])
        return mass

    def clear_dialog_window(self, dialog:TemperatureCycles):
        if self.table.rowCount() == 0:
            dialog.spin_masa.setValue(0)
            dialog.combo_material.setCurrentIndex(0)

    def extract_dates_table(self):
        total_dates = []
        for row in range(self.table.rowCount()):
            row_dates = []
            for col in range(self.table.columnCount()):
                item = ''
                if col == 0:
                    item = self.table.item(row, col).text()
                elif col == 1:
                    item = self.table.item(row, col).text()
                elif col == 2:
                    item = self.table.item(row, col).text()
                elif col == 3:
                    item = self.table.item(row, col).text()
                elif col == 4:
                    item = self.table.item(row, col).text()
                row_dates.append(item)
            total_dates.append(row_dates)
        return total_dates

    def format_command_profile(self):
        if self.table.rowCount() > 0:
            total_datos = self.extract_dates_table()
            for date in total_datos:
                if date[0] == '0':
                    self._commands.append([f'SET_SP:{date[1]}', f'SET_SOAK:{date[2]}',
                                           'SET_MODE:1'])
                else:
                    self._commands.append([f'SET_RAMP:{date[0]}', f'SET_SP:{date[1]}',
                                           f'SET_SOAK:{date[2]}', 'SET_MODE:2'])

    def send_command_profile(self, wind:Ui_MainWindow):
        self._commands = []
        self.format_command_profile()

        if len(self._commands) > self._index_process:
            for com in self._commands[self._index_process]:
                if 'SET_SP:' in com:
                    wind.lcd_setpoint.display(int(com.split(':')[1]))
                self._ser_op.send_command(com)
            self._index_process += 1
            if len(self._commands) > self._index_process:
                self._commands[self._index_process].append('START:1')
        else:
            self.signal_profile.emit('[END] El proceso completo terminó')
            self._index_process = 0




