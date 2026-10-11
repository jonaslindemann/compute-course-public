"""
Beam calculator with results shown in a QTableView backed by a
QAbstractTableModel (Qt's model/view architecture).
"""

import sys

from qtpy.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTableView, QFormLayout, QVBoxLayout,
)
from qtpy.QtCore import Qt, QAbstractTableModel, QModelIndex

import beam_model_decorators as bm


class BeamTableModel(QAbstractTableModel):
    """Table model exposing x, v(x), V(x) and M(x) of a beam"""

    HEADERS = ["x (m)", "v (m)", "V (N)", "M (Nm)"]

    def __init__(self, beam, n_points=30):
        super().__init__()
        self.beam = beam
        self.n_points = n_points
        self._rows = []
        self._sort_column = 0
        self._sort_order = Qt.SortOrder.AscendingOrder
        self._generate_rows()

    def _generate_rows(self):
        """Compute and cache all rows"""
        self._rows = [
            [x, self.beam.v(x), self.beam.V(x), self.beam.M(x)]
            for x in self.beam.x_values(self.n_points)
        ]
        self._apply_sort()

    def _apply_sort(self):
        """Apply the current sort column and order"""
        reverse = self._sort_order == Qt.SortOrder.DescendingOrder
        self._rows.sort(key=lambda row: row[self._sort_column], reverse=reverse)

    def refresh(self):
        """Recompute the table when the beam has changed"""
        self.beginResetModel()
        self._generate_rows()
        self.endResetModel()

    # --- QAbstractTableModel interface

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return f"{self._rows[index.row()][index.column()]:.5g}"
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.HEADERS[section]
            return str(section)
        return None

    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        """Called by the view when a column header is clicked"""
        self.layoutAboutToBeChanged.emit()
        self._sort_column = column
        self._sort_order = order
        self._apply_sort()
        self.layoutChanged.emit()


class BeamWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """BeamWindow constructor"""
        super().__init__()

        # Create model instances

        self.beam = bm.BeamSimplySupported()
        self.table_model = BeamTableModel(self.beam)

        # Configure window

        self.resize(500, 600)
        self.move(50, 50)
        self.setWindowTitle("Beam calculator")

        # Create controls

        self.a_edit = QLineEdit()
        self.b_edit = QLineEdit()
        self.P_edit = QLineEdit()
        self.E_edit = QLineEdit()
        self.I_edit = QLineEdit()

        self.beam_table = QTableView()
        self.beam_table.setModel(self.table_model)
        self.beam_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.beam_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.beam_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.beam_table.verticalHeader().setVisible(False)
        self.beam_table.horizontalHeader().setStretchLastSection(True)
        self.beam_table.setSortingEnabled(True)
        self.beam_table.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.beam_table.setAlternatingRowColors(True)

        # Layout

        form = QFormLayout()
        form.addRow("a (m)", self.a_edit)
        form.addRow("b (m)", self.b_edit)
        form.addRow("P (N)", self.P_edit)
        form.addRow("E (Pa)", self.E_edit)
        form.addRow("I (m⁴)", self.I_edit)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.beam_table)

        # Connect signals to event methods

        self.a_edit.editingFinished.connect(self.on_editing_finished)
        self.b_edit.editingFinished.connect(self.on_editing_finished)
        self.P_edit.editingFinished.connect(self.on_editing_finished)
        self.E_edit.editingFinished.connect(self.on_editing_finished)
        self.I_edit.editingFinished.connect(self.on_editing_finished)

        # Fill controls with values from the model

        self.update_controls()
        self.beam_table.resizeColumnsToContents()

    def update_controls(self) -> None:
        """Model -> controls"""

        self.a_edit.setText(str(self.beam.a))
        self.b_edit.setText(str(self.beam.b))
        self.P_edit.setText(str(self.beam.P))
        self.E_edit.setText(str(self.beam.E))
        self.I_edit.setText(str(self.beam.I))

        self.table_model.refresh()

    def update_model(self) -> None:
        """Controls -> model. Invalid values are ignored by the model."""

        self.beam.a = self.a_edit.text()
        self.beam.b = self.b_edit.text()
        self.beam.P = self.P_edit.text()
        self.beam.E = self.E_edit.text()
        self.beam.I = self.I_edit.text()

    def on_editing_finished(self) -> None:
        """Called when editing of any input field is finished"""

        self.update_model()
        self.update_controls()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = BeamWindow()
    window.show()

    sys.exit(app.exec())
