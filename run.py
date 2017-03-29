#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtQuick import QQuickView, QQuickItem
from PyQt5.QtQml import QJSValue, qmlRegisterType
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent, QQmlEngine

VIEW = None
APP = None
CONTEXT = None

from main import Card, submit_data, VAR_PATH

import logging
logging.basicConfig(level=logging.DEBUG)

# http://pyqt.sourceforge.net/Docs/PyQt5/qml.html
class PyQtShop(QObject):
    def __init__(self, sl="InvalidLink", parent=None):
        logging.info("init shop")
        super().__init__(parent)
        self._shopLink = sl

    @pyqtProperty('QString')
    def shopLink(self):
        return self._shopLink
    @shopLink.setter
    def shopLink(self,link):
        self._shopLink = link

class PyQtShopListModel(QAbstractListModel):
    _data = None
    _ROLE_MAP = {1:QByteArray().append("shopLink")}
    def __init__(self, parent=None):
        logging.info("Init shop list")
        super().__init__(parent)
        self._data = []

        global VIEW
        global APP
        global CONTEXT

        #CONTEXT = VIEW.rootContext()
        #CONTEXT.setContextProperty("submit", submit)
    @pyqtSlot(str)
    def append(self, slink):
        logging.info("Adding shop: " + slink)
        #CONTEXT.setContextProperty("pyqtShopList",
            #QVariant(self))

        #def insertRows(self, row, count, parent=QtCore.QModelIndex()):
            #assert 0 <= row <= self.rowCount()
            #assert count > 0

            #self.beginInsertRows(parent, row, row + count - 1)
            #new_row = [None] * self.columnCount()
            #for row in range(row, row + count):
                #self._data.insert(row, copy(new_row))
            #self.endInsertRows()
        self.beginInsertRows(QModelIndex(),
                self.rowCount(), self.rowCount()+1)

        self._data.append(PyQtShop(slink))
        self.endInsertRows()
        print(self._data)
    @pyqtSlot(QObject)
    def rowCount(self, parent=None):
        count = len(self._data)
        logging.info("Asking rows, returning " + str(count))
        return count
    @pyqtSlot()
    def data(self):
        logging.info("Getting data")
        return None
    def roleNames(self):
        return self._ROLE_MAP



class cardListModel(QObject):
    def __init__(self):
        logging.info("Init cards")

class submitUserInput(QObject):
    shopLinks = []
    cardList = []
    load_signal = pyqtSignal()
    shops = None

    def pyClear(self):
        self.shopLinks.clear()
        self.cardList.clear()

    @pyqtSlot(str)
    def appendShop(self, slink):
        self.shopLinks.append(slink)
    @pyqtSlot(str, str)
    def appendCard(self, name, number):
        c = Card()
        c.name = name
        try:
            c.number = int(number)
        except ValueError:
            c.number = 1
        self.cardList.append(c)
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
    qmlRegisterType(PyQtShop, 'pyqtTypes', 1, 0, 'ShopType')
    #qmlRegisterType(PyQtShopListModel, 'pyqtTypes', 1, 0, 'ShopList')

    submit = submitUserInput()

    CONTEXT = VIEW.rootContext()
    CONTEXT.setContextProperty("submit", submit)

    shops = PyQtShopListModel()
    CONTEXT.setContextProperty("pyqtShopList",
            QVariant(shops))

    url = QUrl('main.qml')
    VIEW.setSource(url)

    VIEW.show()


    sys.exit(APP.exec_())

main()
