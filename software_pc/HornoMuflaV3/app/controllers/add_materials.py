from PySide6.QtWidgets import QDialog, QTableWidgetItem

from app.ui.ui_agregar_material import Ui_Dialog
from app.ui.ui_nuevo_material import Ui_DialogNM
from app.controllers.json_manager import JsonManager

class AddMaterials(QDialog, Ui_Dialog):

    def __init__(self, jm:JsonManager):
        super().__init__()
        self.setupUi(self)
        self.jm = jm
        self.llenar_tabla()
        self.d1 = QDialog()
        self.add_material = Ui_DialogNM()
        self.add_material.setupUi(self.d1)


    def llenar_tabla(self):
        materiales = self.jm.cargar_json()
        filas = len(materiales.keys())
        self.tab_materiales.setRowCount(filas)
        rows = 0
        for name in materiales.keys():
            n = QTableWidgetItem(name)
            dens = QTableWidgetItem(str(materiales[name]['rho']))
            cp = QTableWidgetItem(str(materiales[name]['cp']))
            e = QTableWidgetItem(str(materiales[name]['e']))
            items = [n, dens, cp, e]
            self.tab_materiales.setItem(rows, 0, items[0])
            self.tab_materiales.setItem(rows, 1, items[1])
            self.tab_materiales.setItem(rows, 2, items[2])
            self.tab_materiales.setItem(rows, 3, items[3])
            rows += 1


    def borrar_material(self):
        row = self.tab_materiales.currentRow()
        if self.tab_materiales.rowCount() > 1:
            self.tab_materiales.removeRow(row)
        else:
            self.jm.signal_json_err.emit('[MATERIALES] El cuadro de materiales no puede quedarse vacío')

    def material_extra(self):
        raws = self.tab_materiales.rowCount()
        self.tab_materiales.setRowCount(raws + 1)
        name = QTableWidgetItem(self.add_material.line_nombreMaterial.text())
        dens = QTableWidgetItem(self.add_material.spin_densidad.text())
        cp = QTableWidgetItem(self.add_material.spin_calorEsp.text())
        e = QTableWidgetItem(self.add_material.spin_emis.text())
        self.tab_materiales.setItem(raws, 0, name)
        self.tab_materiales.setItem(raws, 1, dens)
        self.tab_materiales.setItem(raws, 2, cp)
        self.tab_materiales.setItem(raws, 3, e)


    def guardar_material_json(self):
        raws = self.tab_materiales.rowCount()
        dict_mat = {}
        for r in range(raws):
            name = self.tab_materiales.item(r, 0).text()
            aux = {}
            aux['rho'] = float(self.tab_materiales.item(r, 1).text())
            aux['cp'] = float(self.tab_materiales.item(r, 2).text())
            aux['e'] = float(self.tab_materiales.item(r, 3).text())
            dict_mat[name] = aux
        self.jm.guardar_json(dict_mat)



