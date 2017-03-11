#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtQuick import QQuickView

VIEW = None
APP = None

from main import Card, submit_data

import logging
logging.basicConfig(level=logging.DEBUG)

class Card(object):
    name = ""
    number = ""
    def __str__(self):
        return self.name + " : " + str(self.number)

class submitUserInput(QObject):
    shopLinks = []
    cardList = []

    @pyqtSlot(str, str)
    def appendCard(self, name, number):
        c = Card()
        c.name = name
        try:
            c.number = int(number)
        except ValueError:
            c.number = 1
        self.cardList.append(c)
    @pyqtSlot(str)
    def appendShop(self, slink):
        self.shopLinks.append(slink)
    @pyqtSlot()
    def clicked(self):
        logging.info("Clicked!")
        result_page = submit_data(self.shopLinks, self.cardList)
        QDesktopServices.openUrl( QUrl(result_page) )

def main():
    global VIEW
    global APP
    APP = QGuiApplication(sys.argv)
    VIEW = QQuickView()
    url = QUrl('main.qml')
    VIEW.setSource(url)


    submit = submitUserInput()

    context = VIEW.rootContext()
    context.setContextProperty("submit", submit)
    VIEW.show()


    sys.exit(APP.exec_())

main()
