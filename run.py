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
SHOP_LIST = None
CARD_LIST = None

from main import Card, submit_data, VAR_PATH

import logging
logging.basicConfig(level=logging.DEBUG)

# http://pyqt.sourceforge.net/Docs/PyQt5/qml.html
class PyQtShop(QObject):
    _shopLink = ""
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
    @pyqtSlot(str)
    def append(self, slink):
        logging.info("Adding shop: " + slink)
        self.beginInsertRows(QModelIndex(),
                self.rowCount(), self.rowCount())

        self._data.append(PyQtShop(slink))
        self.endInsertRows()
        print(self._data)
    @pyqtSlot(QObject)
    def rowCount(self, parent=None):
        count = len(self._data)
        logging.info("Asking rows, returning " + str(count))
        return count
    def dewrap(self, i):
        return self._data[i]._shopLink

    @pyqtSlot(QModelIndex, int)
    def data(self, index, role):
        i = index.row()
        logging.info("Getting data " + str(i))
        assert(role == 1)
        return QVariant( self.dewrap(i)  )

# http://stackoverflow.com/q/29455801/1166518
    def roleNames(self):
        return self._ROLE_MAP


def _dict_to_rolemap(d):
    ret = {}
    for k, v in d.items():
        ret[k] = QByteArray().append(v)
    return ret
class PyQtCardListModel(QAbstractListModel):
    _data = None
    _ROLE_MAP = _dict_to_rolemap({1:"name", 2:"number"})
    def __init__(self, parent=None):
        logging.info("Init cards")
        super().__init__(parent)
        self._data = []
    @pyqtSlot(str, str)
    def append(self, name, number):
        logging.info("Adding card: " + name + " " + number)
        self.beginInsertRows(QModelIndex(),
                self.rowCount(), self.rowCount())
        c = Card()
        c.name = name
        try:
            c.number = int(number)
        except ValueError:
            c.number = 1
        self._data.append(c)
        self.endInsertRows()
        print(self._data)
    @pyqtSlot(QObject)
    def rowCount(self, parent=None):
        count = len(self._data)
        logging.info("Asking rows, returning " + str(count))
        return count
    @pyqtSlot(QModelIndex, int)
    def data(self, index, role):
        i = index.row()
        logging.info("Getting card data " + str(i))
        assert (role == 1 or role == 2)
        ret = ""
        if role == 1:
            ret = self._data[i].name
        if role == 2:
            ret = self._data[i].number
        logging.info("got " + str(ret))
        return QVariant(ret)
    def roleNames(self):
        return self._ROLE_MAP

class submitUserInput(QObject):
    cardList = []
    load_signal = pyqtSignal()
    shops = None

    def pyClear(self):
        self.shopLinks.clear()
        self.cardList.clear()

    @pyqtSlot()
    def clicked(self):
        logging.info("Clicked!")
        global SHOP_LIST
        global CARD_LIST
        result_page = submit_data(
            [SHOP_LIST.dewrap(i) for i in range(SHOP_LIST.rowCount())],
            CARD_LIST._data)
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
    global SHOP_LIST
    global CARD_LIST
    APP = QGuiApplication(sys.argv)
    VIEW = QQuickView()
    qmlRegisterType(PyQtShop, 'pyqtTypes', 1, 0, 'ShopType')
    #qmlRegisterType(PyQtShopListModel, 'pyqtTypes', 1, 0, 'ShopList')

    submit = submitUserInput()

    CONTEXT = VIEW.rootContext()
    CONTEXT.setContextProperty("submit", submit)

    SHOP_LIST = PyQtShopListModel()
    CONTEXT.setContextProperty("pyqtShopList",
            QVariant(SHOP_LIST))

    CARD_LIST = PyQtCardListModel()
    CONTEXT.setContextProperty("pyqtCardList",
            QVariant(CARD_LIST))

    url = QUrl('main.qml')
    VIEW.setSource(url)

    VIEW.show()


    sys.exit(APP.exec_())

main()
