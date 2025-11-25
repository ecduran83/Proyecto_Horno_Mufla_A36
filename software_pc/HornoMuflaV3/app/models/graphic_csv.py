import pyqtgraph as pg
import pandas as pd
import sys
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
# 1. Lee el archivo CSV
df = pd.read_csv('datos_3piezas_950.csv')

# 2. Extrae los datos de las columnas
# Supongamos que el archivo CSV tiene las columnas: Tiempo1, Temp1, Tiempo2, Temp2, Tiempo3, Temp3
# Si las columnas tienen otros nombres, ajústalos aquí
tiempo1 = df['Temperatura Actual_x']
temp1 = df['Temperatura Actual_y']
tiempo2 = df['Setpoint_x']
temp2 = df['Setpoint_y']
tiempo3 = df['Pieza_x']
temp3 = df['Pieza_y']

# 3. Crea la aplicación y la ventana del gráfico
app = pg.mkQApp()
win = pg.GraphicsLayoutWidget(show=True, title="Gráfico de Temperatura")
win.resize(800, 600)
win.setWindowTitle('Gráfico de temperatura')

# 4. Añade una sub-ventana al gráfico
p1 = win.addPlot(title="Temperatura vs Tiempo")
# 5. Grafica cada par de datos
p1.plot(tiempo1, temp1, pen='r', name='Termocupla')
p1.plot(tiempo2, temp2, pen=pg.mkPen('b', style=pg.QtCore.Qt.PenStyle.DashLine), name="Setpoint")
p1.plot(tiempo3, temp3, pen=pg.mkPen('g', style=pg.QtCore.Qt.PenStyle.DashLine), name="Pieza")

# 6. Añade etiquetas y leyendas
p1.setLabel('left', 'Temperatura (°C)')
p1.setLabel('bottom', 'Tiempo (s)')
p1.addLegend()
p1.showGrid(x=True, y=True, alpha=0.3)
# 7. Inicia el bucle de eventos de la aplicación
pg.exec()