import csv
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from calculo_datos import CalculosDatos
# Asumiendo que tienes una clase de ventana principal (MainWindow)
# y una lista de datos (data_list) que quieres exportar.

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # ... tu código para configurar la ventana ...
        self.calculo = CalculosDatos()
        self.button_save = QPushButton("Guardar como CSV", self)
        self.button_save.clicked.connect(self.guardar_csv)
        self.thermal_profile = [
            {'tipo': 'normal', 'temp_obj_C': 950.0},
            {'tipo': 'meseta', 'duracion_min': 30.0},
        ]
        self.material = [7850, 470, 0.75]
        # Asume que data_list es una lista de tus datos
        self.data_list = self.calculo.pid_temp_masa_tiempo(self.thermal_profile, self.material, 0.36, 77.5)

    def guardar_csv(self):
        # Abrir el diálogo para guardar el archivo
        options = QFileDialog.Options()
        # El filtro asegura que solo se muestren archivos .csv
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo CSV", "",
                                                   "Archivos CSV (*.csv);;Todos los archivos (*)", options=options)

        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for row in self.data_list:
                    csv_writer.writerow(row)
            print(f"Datos guardados en {file_path}")

# Este es un ejemplo de cómo podrías usarlo (no se incluyen todos los detalles de PyQt)
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()