# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nuevo_materialAKJagz.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QDoubleSpinBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_DialogNM(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(314, 222)
        Dialog.setMinimumSize(QSize(314, 222))
        Dialog.setMaximumSize(QSize(314, 222))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.line_nombreMaterial = QLineEdit(Dialog)
        self.line_nombreMaterial.setObjectName(u"line_nombreMaterial")

        self.gridLayout.addWidget(self.line_nombreMaterial, 1, 1, 1, 1)

        self.spin_densidad = QDoubleSpinBox(Dialog)
        self.spin_densidad.setObjectName(u"spin_densidad")

        self.gridLayout.addWidget(self.spin_densidad, 2, 1, 1, 1)

        self.spin_calorEsp = QDoubleSpinBox(Dialog)
        self.spin_calorEsp.setObjectName(u"spin_calorEsp")

        self.gridLayout.addWidget(self.spin_calorEsp, 3, 1, 1, 1)

        self.spin_emis = QDoubleSpinBox(Dialog)
        self.spin_emis.setObjectName(u"spin_emis")

        self.gridLayout.addWidget(self.spin_emis, 4, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nuevo Material", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Densidad (kg/m3):", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Calor Espec\u00edco J/Kg-K:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Emisividad [0-1]:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Material (Nombre):", None))
        self.line_nombreMaterial.setPlaceholderText(QCoreApplication.translate("Dialog", u"Nombre de Material", None))
    # retranslateUi

