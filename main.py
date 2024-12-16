"""
NOM : GULZAR
PRÉNOM : ZIA
SECTION : B1-INFO
MATRICULE : 000595624
"""
from window import MyWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QMessageBox, QFileDialog, QLabel
from PySide6.QtGui import QImage, QPixmap, QColor
from encoding import Decoder
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())