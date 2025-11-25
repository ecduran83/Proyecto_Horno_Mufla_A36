# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowgFhFcc.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLCDNumber, QLabel,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
import app.assets.resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(889, 581)
        self.action_abrirGrafico = QAction(MainWindow)
        self.action_abrirGrafico.setObjectName(u"action_abrirGrafico")
        self.action_ExportarCSV = QAction(MainWindow)
        self.action_ExportarCSV.setObjectName(u"action_ExportarCSV")
        self.action_ExportarPNG = QAction(MainWindow)
        self.action_ExportarPNG.setObjectName(u"action_ExportarPNG")
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.action_ajustarPID = QAction(MainWindow)
        self.action_ajustarPID.setObjectName(u"action_ajustarPID")
        self.actionPrueba_Paso_en_Potencia = QAction(MainWindow)
        self.actionPrueba_Paso_en_Potencia.setObjectName(u"actionPrueba_Paso_en_Potencia")
        self.action_salir = QAction(MainWindow)
        self.action_salir.setObjectName(u"action_salir")
        self.actionAgregar_Material = QAction(MainWindow)
        self.actionAgregar_Material.setObjectName(u"actionAgregar_Material")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_conectar = QPushButton(self.groupBox)
        self.btn_conectar.setObjectName(u"btn_conectar")

        self.horizontalLayout_6.addWidget(self.btn_conectar)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_6.addWidget(self.label)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.lcd_setpoint = QLCDNumber(self.groupBox_5)
        self.lcd_setpoint.setObjectName(u"lcd_setpoint")

        self.horizontalLayout_7.addWidget(self.lcd_setpoint)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.lcd_tempActual = QLCDNumber(self.groupBox_5)
        self.lcd_tempActual.setObjectName(u"lcd_tempActual")

        self.horizontalLayout_7.addWidget(self.lcd_tempActual)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)
        self.horizontalLayout_7.setStretch(2, 1)
        self.horizontalLayout_7.setStretch(3, 2)

        self.horizontalLayout_2.addWidget(self.groupBox_5)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tab_potenciaFija = QTabWidget(self.groupBox_3)
        self.tab_potenciaFija.setObjectName(u"tab_potenciaFija")
        self.tab_setpoint = QWidget()
        self.tab_setpoint.setObjectName(u"tab_setpoint")
        self.verticalLayout_9 = QVBoxLayout(self.tab_setpoint)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_4 = QLabel(self.tab_setpoint)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u":/logo_mecatronica_inv.png"))
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_4)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, -1, -1, -1)
        self.label_6 = QLabel(self.tab_setpoint)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.spin_setpoint = QSpinBox(self.tab_setpoint)
        self.spin_setpoint.setObjectName(u"spin_setpoint")
        self.spin_setpoint.setMaximum(1000)

        self.gridLayout_3.addWidget(self.spin_setpoint, 0, 1, 1, 1)

        self.label_5 = QLabel(self.tab_setpoint)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.bar_potenciaSetpoint = QProgressBar(self.tab_setpoint)
        self.bar_potenciaSetpoint.setObjectName(u"bar_potenciaSetpoint")
        self.bar_potenciaSetpoint.setValue(24)

        self.gridLayout_3.addWidget(self.bar_potenciaSetpoint, 1, 1, 1, 1)

        self.btn_iniciarSetpoint = QPushButton(self.tab_setpoint)
        self.btn_iniciarSetpoint.setObjectName(u"btn_iniciarSetpoint")

        self.gridLayout_3.addWidget(self.btn_iniciarSetpoint, 2, 1, 1, 1)

        self.btn_enviarSetpoint = QPushButton(self.tab_setpoint)
        self.btn_enviarSetpoint.setObjectName(u"btn_enviarSetpoint")

        self.gridLayout_3.addWidget(self.btn_enviarSetpoint, 2, 0, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)

        self.verticalLayout_9.addLayout(self.gridLayout_3)

        self.verticalLayout_9.setStretch(0, 2)
        self.verticalLayout_9.setStretch(1, 1)
        self.tab_potenciaFija.addTab(self.tab_setpoint, "")
        self.tab_rampaMeseta = QWidget()
        self.tab_rampaMeseta.setObjectName(u"tab_rampaMeseta")
        self.verticalLayout_8 = QVBoxLayout(self.tab_rampaMeseta)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_agregar_etapa = QPushButton(self.tab_rampaMeseta)
        self.btn_agregar_etapa.setObjectName(u"btn_agregar_etapa")

        self.horizontalLayout_8.addWidget(self.btn_agregar_etapa)

        self.btn_eliminar_etapa = QPushButton(self.tab_rampaMeseta)
        self.btn_eliminar_etapa.setObjectName(u"btn_eliminar_etapa")

        self.horizontalLayout_8.addWidget(self.btn_eliminar_etapa)

        self.btn_eliminar_perfil = QPushButton(self.tab_rampaMeseta)
        self.btn_eliminar_perfil.setObjectName(u"btn_eliminar_perfil")

        self.horizontalLayout_8.addWidget(self.btn_eliminar_perfil)


        self.verticalLayout_8.addLayout(self.horizontalLayout_8)

        self.tab_agregarPerfil = QTableWidget(self.tab_rampaMeseta)
        if (self.tab_agregarPerfil.columnCount() < 5):
            self.tab_agregarPerfil.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tab_agregarPerfil.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tab_agregarPerfil.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tab_agregarPerfil.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tab_agregarPerfil.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tab_agregarPerfil.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tab_agregarPerfil.setObjectName(u"tab_agregarPerfil")
        self.tab_agregarPerfil.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tab_agregarPerfil.setSupportedDragActions(Qt.DropAction.IgnoreAction)

        self.verticalLayout_8.addWidget(self.tab_agregarPerfil)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.bar_potenciaPerfil = QProgressBar(self.tab_rampaMeseta)
        self.bar_potenciaPerfil.setObjectName(u"bar_potenciaPerfil")
        self.bar_potenciaPerfil.setValue(24)

        self.gridLayout_6.addWidget(self.bar_potenciaPerfil, 0, 1, 1, 1)

        self.btn_enviarPerfil = QPushButton(self.tab_rampaMeseta)
        self.btn_enviarPerfil.setObjectName(u"btn_enviarPerfil")

        self.gridLayout_6.addWidget(self.btn_enviarPerfil, 1, 0, 1, 1)

        self.label_7 = QLabel(self.tab_rampaMeseta)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_6.addWidget(self.label_7, 0, 0, 1, 1)

        self.btn_iniciarPerfil = QPushButton(self.tab_rampaMeseta)
        self.btn_iniciarPerfil.setObjectName(u"btn_iniciarPerfil")

        self.gridLayout_6.addWidget(self.btn_iniciarPerfil, 1, 1, 1, 1)

        self.gridLayout_6.setColumnStretch(0, 1)

        self.verticalLayout_8.addLayout(self.gridLayout_6)

        self.tab_potenciaFija.addTab(self.tab_rampaMeseta, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.bar_potenciaFija = QProgressBar(self.tab)
        self.bar_potenciaFija.setObjectName(u"bar_potenciaFija")
        self.bar_potenciaFija.setValue(24)

        self.gridLayout.addWidget(self.bar_potenciaFija, 1, 1, 1, 1)

        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)

        self.btn_iniciarPotenciaFija = QPushButton(self.tab)
        self.btn_iniciarPotenciaFija.setObjectName(u"btn_iniciarPotenciaFija")

        self.gridLayout.addWidget(self.btn_iniciarPotenciaFija, 2, 1, 1, 1)

        self.btn_enviarPotenciaFija = QPushButton(self.tab)
        self.btn_enviarPotenciaFija.setObjectName(u"btn_enviarPotenciaFija")

        self.gridLayout.addWidget(self.btn_enviarPotenciaFija, 2, 0, 1, 1)

        self.spin_potenciaFija = QSpinBox(self.tab)
        self.spin_potenciaFija.setObjectName(u"spin_potenciaFija")
        self.spin_potenciaFija.setMaximum(2500)

        self.gridLayout.addWidget(self.spin_potenciaFija, 0, 1, 1, 1)

        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_3.addLayout(self.gridLayout)

        self.tab_potenciaFija.addTab(self.tab, "")

        self.verticalLayout_7.addWidget(self.tab_potenciaFija)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.grafica = PlotWidget(self.groupBox_4)
        self.grafica.setObjectName(u"grafica")

        self.verticalLayout_10.addWidget(self.grafica)


        self.horizontalLayout.addWidget(self.groupBox_4)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.log_consola = QPlainTextEdit(self.groupBox_2)
        self.log_consola.setObjectName(u"log_consola")
        self.log_consola.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.log_consola)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 889, 22))
        self.menuHerramientas_2 = QMenu(self.menubar)
        self.menuHerramientas_2.setObjectName(u"menuHerramientas_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHerramientas_2.menuAction())
        self.menuHerramientas_2.addAction(self.action_ajustarPID)
        self.menuHerramientas_2.addAction(self.actionAgregar_Material)

        self.retranslateUi(MainWindow)

        self.tab_potenciaFija.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Horno Mufla UMSA", None))
        self.action_abrirGrafico.setText(QCoreApplication.translate("MainWindow", u"Abrir gr\u00e1fico", None))
        self.action_ExportarCSV.setText(QCoreApplication.translate("MainWindow", u"Exportar gr\u00e1fico CSV", None))
        self.action_ExportarPNG.setText(QCoreApplication.translate("MainWindow", u"Exportar Imagen PNG", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.action_ajustarPID.setText(QCoreApplication.translate("MainWindow", u"Ajustar constantes PID", None))
        self.actionPrueba_Paso_en_Potencia.setText(QCoreApplication.translate("MainWindow", u"Prueba Paso en Potencia", None))
        self.action_salir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionAgregar_Material.setText(QCoreApplication.translate("MainWindow", u"Agregar Material", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Conexi\u00f3n", None))
        self.btn_conectar.setText(QCoreApplication.translate("MainWindow", u"Conectar", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Desconectado", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Temperaturas", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Temp. Setpoint:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Temp. Actual:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Ajustes", None))
        self.label_4.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Potencia (%):", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Setpoin (\u00baC)", None))
        self.btn_iniciarSetpoint.setText(QCoreApplication.translate("MainWindow", u"Iniciar", None))
        self.btn_enviarSetpoint.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.tab_potenciaFija.setTabText(self.tab_potenciaFija.indexOf(self.tab_setpoint), QCoreApplication.translate("MainWindow", u"Setpoint", None))
        self.btn_agregar_etapa.setText(QCoreApplication.translate("MainWindow", u"A\u00f1adir Perfil", None))
        self.btn_eliminar_etapa.setText(QCoreApplication.translate("MainWindow", u"Eliminar Fila", None))
        self.btn_eliminar_perfil.setText(QCoreApplication.translate("MainWindow", u"Eliminar Todo", None))
        ___qtablewidgetitem = self.tab_agregarPerfil.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Velocidad (\u00baC/min)", None));
        ___qtablewidgetitem1 = self.tab_agregarPerfil.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Setpoint (\u00baC)", None));
        ___qtablewidgetitem2 = self.tab_agregarPerfil.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Meseta (min)", None));
        ___qtablewidgetitem3 = self.tab_agregarPerfil.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Masa (kg)", None));
        ___qtablewidgetitem4 = self.tab_agregarPerfil.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Material", None));
        self.btn_enviarPerfil.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Potencia (%):", None))
        self.btn_iniciarPerfil.setText(QCoreApplication.translate("MainWindow", u"Iniciar", None))
        self.tab_potenciaFija.setTabText(self.tab_potenciaFija.indexOf(self.tab_rampaMeseta), QCoreApplication.translate("MainWindow", u"Rampas y Mesetas", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Esta opcion env\u00eda una cantidad fija de\n"
"potencia, por lo que no es recomendable\n"
"enviar mas de 600 W, ya que el equipo\n"
"podr\u00eda llegar a mas de 1000 \u00baC.\n"
"", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Potencia (%):", None))
        self.btn_iniciarPotenciaFija.setText(QCoreApplication.translate("MainWindow", u"Iniciar", None))
        self.btn_enviarPotenciaFija.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Potencia Set:", None))
        self.tab_potenciaFija.setTabText(self.tab_potenciaFija.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Potencia Fija", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Temperatura vs. Tiempo", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Informaci\u00f3n", None))
        self.menuHerramientas_2.setTitle(QCoreApplication.translate("MainWindow", u"Herramientas", None))
    # retranslateUi

