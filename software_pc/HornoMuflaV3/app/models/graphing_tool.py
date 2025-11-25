from pyqtgraph import PlotWidget
from app.models.calculo_datos import CalculosDatos
import pyqtgraph as pg

class GraphingTool:
    def __init__(self, grafica:PlotWidget):
        self.grafica = grafica
        self.grafica.setBackground('w')
        self.grafica.setLabel('left', 'Temperatura °C')
        self.grafica.setLabel('bottom', 'Tiempo (s)')
        self.grafica.showGrid(x=True, y=True)
        self.plot_item = grafica.plot(pen='r', name='Temperatura Actual')
        self.plotData = None
        self.calculo = CalculosDatos()
        self.T_actual = []
        self.t_actual = []
        self.current_second = 0

    def graficar_setpoint(self, setpoint, t_e):
        self.clear_plot()
        [T_sp, t] = self.calculo.temp_setpoint(setpoint, t_e)
        self.grafica.plot(t, T_sp, pen=pg.mkPen('b', style=pg.QtCore.Qt.PenStyle.DashLine),
                               name="Setpoint (Referencia)")

    def graficar_perfil(self, thermal_profile, material, mass, t_amb):
        self.clear_plot()
        [T_t, T_p, t] = self.calculo.pid_temp_masa_tiempo(thermal_profile, material, mass, t_amb)
        self.grafica.plot(t, T_t, pen=pg.mkPen('b', style=pg.QtCore.Qt.PenStyle.DashLine),
                               name="Setpoint")
        self.grafica.plot(t, T_p, pen=pg.mkPen('g', style=pg.QtCore.Qt.PenStyle.DashLine),
                               name="Pieza")

    def graficar_real_time(self, temp):
        self.T_actual.append(temp)
        self.t_actual.append(self.current_second)
        self.plot_item.setData(x=self.t_actual, y=self.T_actual)
        self.current_second += 1

    def clear_plot(self):
        for item in self.grafica.listDataItems():
            item.clear()
        self.T_actual = []
        self.t_actual = []
        self.current_second = 0

    def fix_grafic(self):
        self.clear_plot()
        self.grafica.plot([0], [0], pen=pg.mkPen('b', style=pg.QtCore.Qt.PenStyle.DashLine),
                          name="Setpoint")
        self.grafica.setXRange(0, 3600)
