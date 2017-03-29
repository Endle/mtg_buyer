import QtQuick 2.7
import QtQuick.Controls 2.1
//import pyqtTypes 1.0

Rectangle {
    width: 800
    height: 600



    TextField {
        id: addShopLinkTextField
        x: 97
        y: 114
        width: 269
        height: 40
        text: qsTr("Shop Link")
    }
    Button {
        id: addShopLinkButton
        x: 97
        y: 175
        width: 115
        height: 40
        text: qsTr("Add Shop Link")
        onClicked: {
            pyqtShopList.append(addShopLinkTextField.text);
            addShopLinkTextField.clear();
        }
    }
    Rectangle {
        id: rectangle
        border.width: 1
        border.color: "#000000"
        width: 269
        height: 226
        x: 97
        y: 236

        ListView {
            id: shop_listView
            x: 0
            y: 0
            width: 261
            height: 226

            delegate: Item {
                x: 5
                width: 80
                height: 40
                Row {
                    Text {text: shopLink}
                }
            }


            model: pyqtShopList
                /*
                ListModel {
                id: shopListModel
                objectName: "shopListModel"
                /*
                ListElement {
                    shopLink: "https://shop34266771.taobao.com/"
                }
                ListElement {
                   shopLink: "https://shop101650459.taobao.com/"
                }

                function loadShopList() {
                    console.log("loading in qml" + link);
                    var list = Object.create(ShopList);
                    console.log(list);
                    var link = "http://baidu.com"
                    pyqtShopList.append(link);
                }
                function add(link) {
                    console.log("add shop");
                    var shop = Object.create(ShopType);
                    shop.shopLink = link;
                    shopListModel.append(shop);
                }
            }   */

        }
    }

    Rectangle{
        x: 385
        y: 236
        width: 309
        height: 226
        border.width: 1
        border.color: "#000000"
    ListView {
        id: card_listView
        x: 0
        y: 0
        width: 321
        height: 226
        delegate: Item {
            x: 5
            width: 80
            height: 40
            Row {
                Text {text: name +  " : " + number}
            }
        }
        model: pyqtCardList
        /*
        model: ListModel {
            id: cardListModel
            ListElement {
                name: "闪电击"
                number: "3"
            }
            ListElement {
                name: "反抗烈炬茜卓"
                number: "2"
            }
            ListElement {
                name: "生机巨械"
                number: "4"
            }
        }
        */
    }
    }
    TextField {
        id: addCardNameTextField
        x: 385
        y: 114
        width: 215
        height: 40
        text: qsTr("Card Name")
    }

    TextField {
        id: addCardNumberTextField
        x: 626
        y: 114
        width: 68
        height: 40
        text: qsTr("Number")
    }
    Button {
        id: addCardButton
        x: 579
        y: 175
        width: 115
        height: 40
        text: qsTr("Add Card")
        onClicked: {
            pyqtCardList.append(addCardNameTextField.text, addCardNumberTextField.text)
            addCardNameTextField.clear()
            addCardNumberTextField.clear()
        }
    }


    Button {
        id: submitUserInputButton
        x: 534
        y: 468
        width: 160
        height: 45
        text: qsTr("Submit")
        //i: 0
        onClicked: {
            var i;
            /*
            for(i=0; i<shopListModel.count; i++) {
                submit.appendShop( shopListModel.get(i).shopLink );
            }

            for(i=0; i<cardListModel.count; i++) {
                submit.appendCard( cardListModel.get(i).name, cardListModel.get(i).number)
            }
*/
            submit.clicked()
        }
    }

    Button {
        id: loadFromFileButton
        x: 97
        y: 473
        width: 100
        height: 45
        text: qsTr("Load Shop")
        onClicked: {
            //shopListModel.loadShopList()
            //submit.loadShopListFromFile(shop_listView.loadShopList)
            pyqtShopList.append("baidu.com");

        }
    }

    Button {
        id: saveToFileButton
        x: 264
        y: 473
        width: 100
        height: 45
        text: qsTr("Save Shop")
        onClicked: {
            submit.saveShopListToFile()
        }
    }
}
