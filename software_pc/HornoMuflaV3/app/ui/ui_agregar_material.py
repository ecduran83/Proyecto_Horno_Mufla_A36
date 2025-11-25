# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'agregar_materialdpTFsI.ui'
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
    QGridLayout, QHeaderView, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(664, 231)
        Dialog.setMinimumSize(QSize(664, 231))
        Dialog.setMaximumSize(QSize(664, 16777215))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.btn_eliminarMaterial = QPushButton(Dialog)
        self.btn_eliminarMaterial.setObjectName(u"btn_eliminarMaterial")

        self.gridLayout.addWidget(self.btn_eliminarMaterial, 1, 1, 1, 1)

        self.btn_agregarMaterial = QPushButton(Dialog)
        self.btn_agregarMaterial.setObjectName(u"btn_agregarMaterial")

        self.gridLayout.addWidget(self.btn_agregarMaterial, 0, 1, 1, 1)

        self.tab_materiales = QTableWidget(Dialog)
        if (self.tab_materiales.columnCount() < 4):
            self.tab_materiales.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tab_materiales.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tab_materiales.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tab_materiales.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tab_materiales.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tab_materiales.setObjectName(u"tab_materiales")
        self.tab_materiales.setMinimumSize(QSize(563, 181))
        self.tab_materiales.setMaximumSize(QSize(563, 16777215))
        self.tab_materiales.horizontalHeader().setDefaultSectionSize(140)

        self.gridLayout.addWidget(self.tab_materiales, 0, 0, 3, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Agregar Material", None))
        self.btn_eliminarMaterial.setText(QCoreApplication.translate("Dialog", u"Eliminar", None))
        self.btn_agregarMaterial.setText(QCoreApplication.translate("Dialog", u"Nuevo", None))
        ___qtablewidgetitem = self.tab_materiales.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Nombre", None));
        ___qtablewidgetitem1 = self.tab_materiales.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Densidad (kg/m3)", None));
        ___qtablewidgetitem2 = self.tab_materiales.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Calor Espec\u00edfico (J/kg-K)", None));
        ___qtablewidgetitem3 = self.tab_materiales.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Emisividad [0-1]", None));
    # retranslateUi

