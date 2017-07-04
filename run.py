#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from pathlib import Path
import pathlib

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
# 这个类隐藏在 QAbstractItemModel 后面，其实没必要定义
# FIXME 下次无聊的时候重构掉
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
    def clear(self):
        self.beginRemoveRows(QModelIndex(),
                0, self.rowCount()-1)
        self._data.clear()
        self.endRemoveRows()
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
    def getStrList(self):
        return [self.dewrap(i) for i in range(self.rowCount())]

# http://stackoverflow.com/q/29455801/1166518
    def roleNames(self):
        return self._ROLE_MAP

    def getShopListFile(self):
        '''Return a Path, showing a file path
        Guarantee that is legal'''
        assert isinstance(VAR_PATH, pathlib.Path)
        path = VAR_PATH.joinpath("shop_list.txt")
        return path

    @pyqtSlot()
    def loadShopListFromFile(self):
        global SHOP_LIST
        path = self.getShopListFile()
        logging.info("loading from " + str(path))
        SHOP_LIST.clear()
        with open(path) as fin:
            for i in fin.readlines():
                SHOP_LIST.append(i)

    @pyqtSlot()
    def saveShopListToFile(self):
        global SHOP_LIST
        path = self.getShopListFile()
        logging.info("saving to " + str(path))
        with open(path, 'w') as fout:
            for i in SHOP_LIST.getStrList():
                print(i, file=fout)


def _dict_to_rolemap(d):
    ret = {}
    for k, v in d.items():
        ret[k] = QByteArray().append(v)
    return ret
class PyQtCardListModel(QAbstractListModel):
    _data = None
    _ROLE_MAP = _dict_to_rolemap({1:"name", 2:"number"})
    def clear(self):
        self.beginRemoveRows(QModelIndex(),
                0, self.rowCount()-1)
        self._data.clear()
        self.endRemoveRows()
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
        logging.info("got {0} via role {1}".format(str(ret), role))
        return QVariant(ret)
    def roleNames(self):
        return self._ROLE_MAP

class submitUserInput(QObject):
    cardList = []
    load_signal = pyqtSignal()
    shops = None
    global SHOP_LIST
    global CARD_LIST

    def pyClear(self):
        SHOP_LIST.clear()
        CARD_LIST.clear()

    @pyqtSlot()
    def clicked(self):
        logging.info("Clicked!")
        shops = SHOP_LIST.getStrList()
        shops = [i.rstrip("\n ?/") for i in shops]
        result_page = submit_data(
            shops,
            CARD_LIST._data)
        self.pyClear()
        #FIXME wrong type
        url = str(result_page)
        logging.warn("open local page " + url)
        QDesktopServices.openUrl( QUrl(url) )


def main():
    global VIEW
    global APP
    global CONTEXT
    global SHOP_LIST
    global CARD_LIST
    APP = QGuiApplication(sys.argv)
    VIEW = QQuickView()

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
