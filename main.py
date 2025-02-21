import sys
import requests

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_ui.ui", self)

        self.ll = "33.082455,68.968649"
        self.spn = "1"

        # params map
        self.server_address_maps = "https://static-maps.yandex.ru/v1?"
        self.map_params = {
            "ll": self.ll,
            "spn": self.spn,
            "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7"
        }

        self.map = make_map(self.server_address_maps, self.map_params)


def make_map(server_address_maps, maps_params):
    response = requests.get(server_address_maps, maps_params)
    if not response:
        return None

    map_file = "map.png"

    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
