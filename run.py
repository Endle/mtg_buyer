#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtQuick import QQuickView, QQuickItem
from PyQt5.QtQml import QJSValue

VIEW = None
APP = None
CONTEXT = None

from main import Card, submit_data, VAR_PATH

import logging
logging.basicConfig(level=logging.DEBUG)

class submitUserInput(QObject):
    shopLinks = []
    cardList = []
    load_signal = pyqtSignal()

    def pyClear(self):
        self.shopLinks.clear()
        self.cardList.clear()

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

    def getShopListFile(self):
        '''Return a Path, showing a file path
        Guarantee that is legal'''
        path = Path(VAR_PATH).joinpath("shop_list.txt")
        return path

    @pyqtSlot('QJSValue')
    def loadShopListFromFile(self, addShop):
        path = self.getShopListFile()
        logging.info("loading from " + str(path))
        print(addShop)
        addShop.call([QJSValue('From PyQt')])
        #self.load_signal = pyqtSignal()
        #global VIEW
        #root = VIEW.rootObject()
        #shopList = root.findChild(QObject, name="shopListModel")
        #print(self.load_signal)
        #print(shopList)
        #self.load_signal.connect("loadShopListSignal")
        #self.load_signal.connect(self.load_signal, shopList)
        #self.load_signal.emit()

    @pyqtSlot()
    def saveShopListToFile(self):
        print("save")

def main():
    global VIEW
    global APP
    global CONTEXT
    APP = QGuiApplication(sys.argv)
    VIEW = QQuickView()
    url = QUrl('main.qml')
    VIEW.setSource(url)


    submit = submitUserInput()

    CONTEXT = VIEW.rootContext()
    CONTEXT.setContextProperty("submit", submit)
    VIEW.show()


    sys.exit(APP.exec_())

main()
