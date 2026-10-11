"""
Common control properties: visible and enabled state, and the button text.
"""

import sys

from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout


class MyWindow(QWidget):
    """Main window class"""

    def __init__(self):
        """MyWindow constructor"""
        super().__init__()

        # Set window properties

        self.setGeometry(300, 300, 400, 80)
        self.setWindowTitle("Button Example")

        # Create button controls

        self.button1 = QPushButton("Hide/show")
        self.button2 = QPushButton("Enable/disable")
        self.button3 = QPushButton("Enabled")

        # Layout

        layout = QHBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        # Connect methods to the clicked signal

        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)

    def on_button1_clicked(self):
        """Toggle visibility of button2"""
        self.button2.setVisible(not self.button2.isVisible())

    def on_button2_clicked(self):
        """Toggle enabled state of button3"""
        if self.button3.isEnabled():
            self.button3.setEnabled(False)
            self.button3.setText("Not enabled")
        else:
            self.button3.setEnabled(True)
            self.button3.setText("Enabled")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
