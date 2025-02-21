import sys
import requests

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_ui.ui", self)

        self.ll = ["33.082455", "68.968649"]
        self.spn = ['0.1']
        self.server_address_maps = "https://static-maps.yandex.ru/v1?"
        self.map_params = {
            "ll": ','.join(self.ll),
            "spn": ','.join(self.spn + self.spn),
            "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7"
        }
        self.make_map(self.server_address_maps, self.map_params)
        self.pixmap = None
        self.label.resize(585, 585)
        self.label.setStyleSheet("background-color: lightgreen")
        self.start.clicked.connect(lambda x: self.make_map(self.server_address_maps, self.map_params))

    def make_map(self, server_address_maps, maps_params):
        response = requests.get(server_address_maps, maps_params)
        if not response:
            print(response.text)
            return None

        map_file = "map.png"

        with open(map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(map_file)
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == 51:
            self.spn = [str(min(0.1, float(self.spn[0]) + 0.01))]
            self.map_params = {
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7"
            }
            self.make_map(self.server_address_maps, self.map_params)
        if event.key() == 57:
            self.spn = [str(max(0.001, float(self.spn[0]) - 0.01))]
            self.map_params = {
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7"
            }
            self.make_map(self.server_address_maps, self.map_params)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
