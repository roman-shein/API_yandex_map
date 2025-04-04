import sys
from tkinter.ttk import Label

import requests

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QLabel


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_ui.ui", self)

        self.ll = ["33.082455", "68.968649"]
        self.spn = ['0.1']
        self.server_address_maps = "https://static-maps.yandex.ru/v1?"
        self.geocoder_server = "https://geocode-maps.yandex.ru/1.x/"
        self.metki = []
        self.map_params = {
            "ll": ','.join(self.ll),
            "spn": ','.join(self.spn + self.spn),
            "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7",
            "theme": "light"
        }
        self.make_map(self.server_address_maps, self.map_params)
        self.pixmap = None
        self.im.resize(585, 585)
        self.im.setStyleSheet("background-color: lightgreen")
        self.start.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.dark.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.light.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.start.clicked.connect(self.search_object)
        self.light.setChecked(True)
        self.dark.toggled.connect(self.theme)
        self.light.toggled.connect(self.theme)
        self.pushButton.clicked.connect(self.reset_metki)

        self.text.returnPressed.connect(self.search_object)

    def theme(self):
        if self.light.isChecked():
            self.map_params["theme"] = "light"
        elif self.dark.isChecked():
            self.map_params["theme"] = "dark"
        self.make_map(self.server_address_maps, self.map_params)

    def make_map(self, server_address_maps, maps_params):
        response = requests.get(server_address_maps, maps_params)
        if not response:
            print(response.text)
            return None

        map_file = "map.png"

        with open(map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(map_file)
        self.im.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        print(event.key())
        # Снимаем фокус с text при нажатии любых стрелочек
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
            self.text.clearFocus()

        if event.key() == Qt.Key.Key_PageDown:
            self.clearFocus()
            self.spn = [str(min(0.1, float(self.spn[0]) + 0.01))]
            self.map_params = {
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7",
                "pt": ','.join(self.metki)
            }
            self.make_map(self.server_address_maps, self.map_params)
        if event.key() == Qt.Key.Key_PageUp:
            self.clearFocus()
            self.spn = [str(max(0.001, float(self.spn[0]) - 0.01))]
            self.map_params = {
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7",
                "pt": ','.join(self.metki)
            }
            self.make_map(self.server_address_maps, self.map_params)
        sme = False
        if event.key() == Qt.Key.Key_Left:
            self.ll[0] = str(float(self.ll[0]) - float(self.spn[0]) / 2)
            sme = True
        if event.key() == Qt.Key.Key_Right:
            self.ll[0] = str(float(self.ll[0]) + float(self.spn[0]) / 2)
            sme = True
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] = str(float(self.ll[1]) + float(self.spn[0]) / 2)
            sme = True
        if event.key() == Qt.Key.Key_Down:
            self.ll[1] = str(float(self.ll[1]) - float(self.spn[0]) / 2)
            sme = True
        if sme:
            self.map_params = {
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7",
                "pt": ','.join(self.metki)
            }
            self.make_map(self.server_address_maps, self.map_params)

    def search_object(self):
        search_text = self.text.text().strip()
        if not search_text:
            return

        geocoder_params = {
            "geocode": search_text,
            "apikey": "7baececd-be0e-4475-a6ae-f15bef0b9622",
            "format": "json"
        }

        try:
            response = requests.get(self.geocoder_server, params=geocoder_params)
            if response.status_code != 200:
                QMessageBox.warning(self, "Ошибка", "Не удалось выполнить запрос к геокодеру")
                return

            data = response.json()

            # Get the first feature
            features = data["response"]["GeoObjectCollection"]["featureMember"]
            if not features:
                QMessageBox.warning(self, "Ошибка", "Объект не найден")
                return

            feature = features[0]["GeoObject"]
            pos = feature["Point"]["pos"]
            self.metki.append(','.join(pos.split() + ["pm2dgl"]))
            self.ll = pos.split()

            # Update map parameters with new coordinates and add marker
            self.map_params.update({
                "ll": ','.join(self.ll),
                "spn": ','.join(self.spn + self.spn),
                "pt": '~'.join(self.metki)
            })
            self.adress.setText(
                feature['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine'])
            self.make_map(self.server_address_maps, self.map_params)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def reset_metki(self):
        self.metki = []
        self.adress.setText('')
        self.map_params.update({
            "ll": ','.join(self.ll),
            "spn": ','.join(self.spn + self.spn),
            "pt": ','.join(self.metki)  # Add marker
        })

        self.make_map(self.server_address_maps, self.map_params)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
