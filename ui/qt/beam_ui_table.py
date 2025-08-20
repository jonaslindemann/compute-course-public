# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:44:29 2016

@author: lindemann
"""

import sys

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

import beam_model_decorators as bm

class NumericDelegate(QStyledItemDelegate):
    """Custom delegate for numeric formatting with decimal alignment"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paint(self, painter, option, index):
        # Get the data
        value = index.data(Qt.DisplayRole)
        
        if value is not None:
            # Set up the style
            painter.save()
            
            # Use the default style but customize alignment
            style = option.widget.style() if option.widget else QApplication.style()
            
            # Modify the option to align right
            opt = QStyleOptionViewItem(option)
            opt.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
            
            # Draw the background
            style.drawControl(QStyle.CE_ItemViewItem, opt, painter, option.widget)
            
            # Draw the text with right alignment
            text_rect = style.subElementRect(QStyle.SE_ItemViewItemText, opt, option.widget)
            painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, str(value))
            
            painter.restore()
        else:
            super().paint(painter, option, index)

class BeamTableModel(QAbstractTableModel):
    """Model for displaying beam calculations in a table"""

    def __init__(self, beam):
        super().__init__()
        self.beam = beam
        self.dx = 0.1  # Step size
        self._data = []  # Cache for data
        self._sort_column = 0
        self._sort_order = Qt.AscendingOrder
        self._generate_data()

    def _generate_data(self):
        """Generate and cache all data"""
        self._data = []
        x = 0.0
        while x <= self.beam.L:
            row_data = [
                x,                    # x position
                self.beam.v(x),      # deflection
                self.beam.V(x),      # shear force
                self.beam.M(x)       # moment
            ]
            self._data.append(row_data)
            x += self.dx
        self._apply_sort()

    def _apply_sort(self):
        """Apply current sorting to data"""
        if self._data:
            reverse = (self._sort_order == Qt.DescendingOrder)
            self._data.sort(key=lambda row: row[self._sort_column], reverse=reverse)

    def refresh_data(self):
        """Refresh data when beam properties change"""
        self.beginResetModel()
        self._generate_data()
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 4  # x, v, V, M

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
            
        if role == Qt.DisplayRole:
            row_data = self._data[index.row()]
            value = row_data[index.column()]
            return f"{value:.5f}"
        elif role == Qt.TextAlignmentRole:
            # Align all numeric data to the right
            return Qt.AlignRight | Qt.AlignVCenter
        return None
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ["x (m)", "v (m)", "V (N)", "M (Nm)"]
                return headers[section]
            elif orientation == Qt.Vertical:
                return str(section)
        elif role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                # Align headers to the right
                return Qt.AlignRight | Qt.AlignVCenter
        return None

    def sort(self, column, order):
        """Sort the data by the given column and order"""
        self.beginResetModel()
        self._sort_column = column
        self._sort_order = order
        self._apply_sort()
        self.endResetModel()

    def flags(self, index):
        """Return item flags - make items selectable and enabled"""
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
class BeamWindow(QWidget):
    """Huvudfönster för programmet"""

    def __init__(self):
        """BeamWindow konstruktor"""
        super().__init__()

        # Skapa modell instans

        self.beam = bm.BeamSimplySupported()

        # Initiera användargränssnitt

        self.setup_ui()

        # Uppdatera kontroller med värden från modell

        self.update_controls()

    def setup_ui(self) -> None:
        """Initiera gränssnitt"""

        self.resize(500, 400)
        self.move(50, 50)
        self.setWindowTitle("Beam calculator")

        # Skapa kontroller

        self.a_label = QLabel("a (m)")
        self.a_edit = QLineEdit()

        self.b_label = QLabel("b (m)")
        self.b_edit = QLineEdit()

        self.P_label = QLabel("P (N)")
        self.P_edit = QLineEdit()

        self.E_label = QLabel("E (Pa)")
        self.E_edit = QLineEdit()

        self.I_label = QLabel("I (Pa)")
        self.I_edit = QLineEdit()

        self.text_edit = QTextEdit("")
        self.text_edit.setFont(QFont("Courier", 10))

        # Skapa layout

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.a_label, 0, 0)
        self.grid.addWidget(self.a_edit,  0, 1)
        self.grid.addItem(QSpacerItem(300, 0), 0, 2)

        self.grid.addWidget(self.b_label, 1, 0)
        self.grid.addWidget(self.b_edit,  1, 1)

        self.grid.addWidget(self.P_label, 2, 0)
        self.grid.addWidget(self.P_edit,  2, 1)

        self.grid.addWidget(self.E_label, 3, 0)
        self.grid.addWidget(self.E_edit,  3, 1)

        self.grid.addWidget(self.I_label, 4, 0)
        self.grid.addWidget(self.I_edit,  4, 1)

        # Result table

        self.beam_table = QTableView()
        self.table_model = BeamTableModel(self.beam)
        self.beam_table.setModel(self.table_model)
        
        # Set custom delegate for numeric formatting
        numeric_delegate = NumericDelegate()
        self.beam_table.setItemDelegate(numeric_delegate)
        
        self.beam_table.setSelectionBehavior(QTableView.SelectRows)
        self.beam_table.setSelectionMode(QTableView.SingleSelection)
        self.beam_table.setEditTriggers(QTableView.NoEditTriggers)
        # self.beam_table.horizontalHeader().setStretchLastSection(True)
        self.beam_table.verticalHeader().setVisible(False)
        self.beam_table.resizeColumnsToContents()
        self.beam_table.resizeRowsToContents()
        self.beam_table.setSortingEnabled(True)
        self.beam_table.setAlternatingRowColors(True)

        self.grid.addWidget(self.beam_table, 5, 0, 2, 0)

        self.grid.setContentsMargins(8, 8, 8, 8)

        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)

        self.setLayout(self.grid)

        # Koppla signaler till händelsemetoder

        self.a_edit.editingFinished.connect(self.on_editing_finished)
        self.b_edit.editingFinished.connect(self.on_editing_finished)
        self.P_edit.editingFinished.connect(self.on_editing_finished)
        self.E_edit.editingFinished.connect(self.on_editing_finished)
        self.I_edit.editingFinished.connect(self.on_editing_finished)

    def update_controls(self) -> None:
        """Fyll kontroller med värden från model"""

        self.a_edit.setText(str(self.beam.a))
        self.b_edit.setText(str(self.beam.b))
        self.P_edit.setText(str(self.beam.P))
        self.E_edit.setText(str(self.beam.E))
        self.I_edit.setText(str(self.beam.I))

        self.table_model.refresh_data()  # Refresh table data
        self.update_text_edit()

    def update_text_edit(self) -> None:
        """Uppdatera text kontroll"""
        self.text_edit.clear()
        self.text_edit.append('{:>10}  {:>10}  {:>10}  {:>10}'.format("x (m)", "v (m)", "V (N)", "M (Nm)"))

        x = 0.0
        dx = 0.1

        while x < self.beam.L + dx:
            self.text_edit.append('{:10.5}  {:10.5}  {:10.5}  {:10.5}'.format(
                x, self.beam.v(x), self.beam.V(x), self.beam.M(x)))
            x += dx

        self.text_edit.moveCursor(QTextCursor.Start)

    def update_model(self) -> None:
        """Uppdatera vår balkmodell från kontroller"""

        self.beam.a = self.a_edit.text()
        self.beam.b = self.b_edit.text()
        self.beam.P = self.P_edit.text()
        self.beam.E = self.E_edit.text()
        self.beam.I = self.I_edit.text()

    def on_editing_finished(self) -> None:
        """Uppdatera när någon kontroll uppdaterats"""

        self.update_model()
        self.update_controls()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = BeamWindow()
    window.show()

    sys.exit(app.exec_())
