from PySide6.QtCore import QTimer
from app.controllers.serial_operations import SerialOperations

class HeartBeat:

    def __init__(self, ser_op:SerialOperations):
        self.heart = QTimer()
        self.time_heart = 2000
        self.ser_op = ser_op
        self.heart.timeout.connect(self.send_heartbeat)


    def start_heart_beat(self):
        self.heart.start(self.time_heart)

    def send_heartbeat(self):
        self.ser_op.send_command('BEAT')

    def stop_heart_beat(self):
        self.heart.stop()

