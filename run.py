#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

VIEW = None
APP = None

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
        c.number = int(number)
        self.cardList.append(c)
    @pyqtSlot(str)
    def appendShop(self, slink):
        self.shopLinks.append(slink)
    @pyqtSlot()
    def clicked(self):
        print("Clicked!")
        print(self.shopLinks)
        for c in self.cardList:
            print(c)

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
