from app.controllers.serial_operations import SerialOperations

class FurnaceOperations:

    def __init__(self, ser_op:SerialOperations):
        self.ser_op = ser_op
        self.is_running = False

    def send_setpoint(self, command):
        comm = f'SET_SP:{command}'
        self.ser_op.send_command(comm)
        self.ser_op.send_command('SET_MODE:0')

    def start_process(self):
        comm = 'START:1'
        self.ser_op.send_command(comm)
        self.is_running = True

    def stop_process(self):
        comm = 'START:0'
        self.ser_op.send_command(comm)
        self.is_running = False

    def send_fix_power(self, command):
        com_num = int((500 * int(command)) / 2500)
        com_str = f'SET_PF:{com_num}'
        self.ser_op.send_command('SET_SP:0')
        self.ser_op.send_command(com_str)
        self.ser_op.send_command('SET_MODE:3')

    def send_constants_pid(self, command):
        kp = f'SET_KP:{command[0]}'
        ki = f'SET_KI:{command[1]}'
        kd = f'SET_KD:{command[2]}'
        self.ser_op.send_command(kp)
        self.ser_op.send_command(ki)
        self.ser_op.send_command(kd)


