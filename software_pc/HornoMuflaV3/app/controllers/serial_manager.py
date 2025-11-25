from PySide6.QtCore import QObject, Signal
from PySide6.QtSerialPort import QSerialPort

class SerialManager(QObject):

    # Patron singleton para la conexion serial
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SerialManager, cls).__new__(cls, *args, **kwargs)

            # Inicializacion unica, se hace una sola vez
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # Evita reinicializar si ya existe
        if getattr(self, '_initialized', False):
            return

        super().__init__()
        self._initialized = True

        # Configuración del puerto
        self.serial = QSerialPort()
        self.serial.readyRead.connect(self._on_ready_read)
        self.serial.errorOccurred.connect(self.error_in_conection)

    # Señales, las cuales son las que interactuan con el resto del programa
    data_received = Signal(str)
    connection_status = Signal(bool)
    wire_desconnection = Signal()

    # Metodos publicos
    def conectar(self, puerto):
        if self.serial.isOpen():
            self.serial.close()

        self.serial.setPortName(puerto)
        self.serial.setBaudRate(QSerialPort.BaudRate.Baud115200)

        if self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            self.connection_status.emit(True)
            return True
        return False

    def desconectar(self):
        if self.serial.isOpen():
            self.serial.close()
            self.connection_status.emit(False)


    # Metodos internos (Slots)
    def _on_ready_read(self):
        while self.serial.canReadLine():
            linea = self.serial.readLine().data().decode().strip()
            if linea:
                # Emitir señal para quien le interese los datos que llegan
                self.data_received.emit(linea)

    def error_in_conection(self, e):
        if e == QSerialPort.SerialPortError.ResourceError:
            self.wire_desconnection.emit()



