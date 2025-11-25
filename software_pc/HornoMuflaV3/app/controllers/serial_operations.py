from app.controllers.serial_manager import SerialManager
from PySide6.QtSerialPort import QSerialPortInfo
from PySide6.QtCore import Signal, QObject

class SerialOperations(QObject):

    device_connected = Signal(str)
    device_not_found_in_list_port = Signal(str)
    device_unconnected = Signal(str)
    temp_received = Signal(float)
    temp_with_process = Signal(float)
    lost_connection = Signal()
    resp_set_controller = Signal(str)
    power_value = Signal(float)
    signal_end_stage = Signal(int)

    def __init__(self):
        super().__init__()
        self._ser_man = SerialManager()
        self._ser_man.data_received.connect(self.process_data)
        self._ser_man.connection_status.connect(self._validate_port)
        self._ser_man.wire_desconnection.connect(self.lost_connection.emit)
        self.device_ok = False
        self._ports_list_ok = []
        self._index_port = 0

    # Función que inicia la validación del dispositivo conectado
    def validate_device(self):
        self._obtain_ports()

    # Escanea y filtra los puertos que solo corresponden a un ESP32
    def _obtain_ports(self):
        if len(self._ports_list_ok) == 0:
            ports_list_object = QSerialPortInfo.availablePorts()
            for port in ports_list_object:
                if 'CP210' in port.description():
                    self._ports_list_ok.append(port.portName())
        self._connect_port()

    # Conecta al puerto correspondiente al indice i en la lista de puertos habilitados
    def _connect_port(self):
        try:
            if len(self._ports_list_ok) > 0:
                self._ser_man.conectar(self._ports_list_ok[self._index_port])
                self._index_port += 1
            else:
                self.device_not_found_in_list_port.emit('[Conexión] El dispositivo no se encontró.')
                self._set_if_without_device()
        except IndexError:
            self.device_not_found_in_list_port.emit('[Conexión] Error en la conexión.')
            self._set_if_without_device()


    # Valida los puertos enviando la llave
    def _validate_port(self, flag):
        if flag:
            self._ser_man.serial.write(self._format_command('HM:UMSA'))
            self._ser_man.serial.flush()
        else:
            self.device_unconnected.emit('[Conexión] Dispositivo desconectado.')

    # Procesa los datos de llegada
    def process_data(self, data):
        if not self.device_ok:
            if data == 'HM:OK':
                self.device_ok = True
                self.device_connected.emit('[Conexión] El dispositivo se conecto correctamente.')
            else:
                self._index_port += 1
                self._ser_man.desconectar()
        else:
            if (('SET_SP:' in data) or ('SET_SOAK:' in data) or ('SET_RAMP:' in data) or
                    ('SET_PF:' in data) or ('SET_MODE:' in data)) or ('SET_K:' in data):
                if data == 'SET_SP:OK':
                    self.resp_set_controller.emit(
                        "[Controlador] Setpoint ajustado correctamente en el controlador")
                elif data == 'SET_SOAK:OK':
                    self.resp_set_controller.emit(
                        "[Controlador] Tiempo de Meseta ajustado correctamente en el controlador")
                elif data == 'SET_RAMP:OK':
                    self.resp_set_controller.emit(
                        "[Controlador] Velocidad de Rampa ajustado correctamente en el controlador")
                elif data == 'SET_PF:OK':
                    self.resp_set_controller.emit(
                        "[Controlador] Potencia fija ajustado correctamente en el controlador")
                elif data == 'SET_MODE:OK':
                    self.resp_set_controller.emit('[Controlador] Tipo de proceso ajustado')
                elif data == 'SET_K:OK':
                    self.resp_set_controller.emit('[Controlador] Las constantes se actualizaron correctamente')
            elif 'START1:' in data:
                self.resp_set_controller.emit('[Controlador] Proceso comenzado correctamente en el controlador')
            elif 'START0:' in data:
                self.resp_set_controller.emit('[Controlador] Proceso detenido correctamente en el controlador')
            elif 'M1:' in data:
                self.resp_set_controller.emit('[Controlador] Etapa de calentamiento con meseta terminada.')
                self.signal_end_stage.emit(1)
            elif 'M2:' in data:
                self.resp_set_controller.emit('[Controlador] Etapa de rampa con meseta terminada')
                self.signal_end_stage.emit(2)
            elif 'TP:' in data:
                temp = float(data.split(':')[1])
                self.temp_with_process.emit(temp)
            elif 'T:' in data:
                temp = float(data.split(':')[1])
                self.temp_received.emit(temp)
            elif 'OU:' in data:
                power = float(data.split(':')[1]) * 100
                self.power_value.emit(power)


    # Formatea la cadena que le llega por parametro a formato listo para enviar
    def _format_command(self, command):
        comm = command + '\n'
        return comm.encode()

    def disconnect_device(self):
        self._set_if_without_device()
        self._ser_man.desconectar()

    def _set_if_without_device(self):
        self._ser_man.desconectar()
        self.device_ok = False
        self._ports_list_ok = []
        self._index_port = 0

    def send_command(self, command):
        self._ser_man.serial.write(self._format_command(command))
        self._ser_man.serial.flush()





