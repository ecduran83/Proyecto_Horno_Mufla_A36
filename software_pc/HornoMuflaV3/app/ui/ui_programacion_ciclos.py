# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'programacion_ciclosGIiXay.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QGridLayout,
    QLabel, QSizePolicy, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 300))
        Dialog.setMaximumSize(QSize(400, 300))
        self.btn_ciclos = QDialogButtonBox(Dialog)
        self.btn_ciclos.setObjectName(u"btn_ciclos")
        self.btn_ciclos.setGeometry(QRect(30, 240, 341, 32))
        sizePolicy.setHeightForWidth(self.btn_ciclos.sizePolicy().hasHeightForWidth())
        self.btn_ciclos.setSizePolicy(sizePolicy)
        self.btn_ciclos.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ciclos.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(-1, -1, 401, 223))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 0)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.check_masa = QCheckBox(self.gridLayoutWidget)
        self.check_masa.setObjectName(u"check_masa")

        self.gridLayout.addWidget(self.check_masa, 0, 0, 1, 1)

        self.check_velocidad = QCheckBox(self.gridLayoutWidget)
        self.check_velocidad.setObjectName(u"check_velocidad")

        self.gridLayout.addWidget(self.check_velocidad, 3, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.spin_velocidad = QSpinBox(self.gridLayoutWidget)
        self.spin_velocidad.setObjectName(u"spin_velocidad")
        self.spin_velocidad.setMaximum(50)

        self.gridLayout.addWidget(self.spin_velocidad, 4, 1, 1, 1)

        self.spin_tiempo_meseta = QSpinBox(self.gridLayoutWidget)
        self.spin_tiempo_meseta.setObjectName(u"spin_tiempo_meseta")
        self.spin_tiempo_meseta.setMaximum(3600)

        self.gridLayout.addWidget(self.spin_tiempo_meseta, 7, 1, 1, 1)

        self.spin_temp_objetivo = QSpinBox(self.gridLayoutWidget)
        self.spin_temp_objetivo.setObjectName(u"spin_temp_objetivo")
        self.spin_temp_objetivo.setMaximum(1000)

        self.gridLayout.addWidget(self.spin_temp_objetivo, 6, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.combo_material = QComboBox(self.gridLayoutWidget)
        self.combo_material.setObjectName(u"combo_material")

        self.gridLayout.addWidget(self.combo_material, 1, 1, 1, 1)

        self.spin_masa = QDoubleSpinBox(self.gridLayoutWidget)
        self.spin_masa.setObjectName(u"spin_masa")
        self.spin_masa.setMaximum(10.000000000000000)

        self.gridLayout.addWidget(self.spin_masa, 2, 1, 1, 1)


        self.retranslateUi(Dialog)
        self.btn_ciclos.accepted.connect(Dialog.accept)
        self.btn_ciclos.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Perfil de Temperatura", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Masa (kg):", None))
        self.check_masa.setText(QCoreApplication.translate("Dialog", u"Con c\u00e1lculo de masa", None))
        self.check_velocidad.setText(QCoreApplication.translate("Dialog", u"Controlar Velocidad", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Tiempo Meseta (min):", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Temp. Objetivo (\u00b0C):", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Velocidad (\u00b0C/min):", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Material", None))
    # retranslateUi

