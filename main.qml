import QtQuick 2.7
import QtQuick.Controls 2.1

Rectangle {
    width: 800
    height: 600


    TextField {
        id: addShopLinkTextField
        x: 97
        y: 114
        width: 238
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
            shopListModel.append({shopLink:addShopLinkTextField.text})
        }
    }
    ListView {
        id: shop_listView
        x: 97
        y: 236
        width: 238
        height: 226
        delegate: Item {
            x: 5
            width: 80
            height: 40
            Row {
                id: row1
                spacing: 10
                Text {
                    text: shopLink
                }
            }
        }
        model: ListModel {
            id: shopListModel
            objectName: "shopListModel"
            ListElement {
                shopLink: "https://shop62237807.taobao.com/"
            }
        }
    }





    ListView {
        id: card_listView
        x: 373
        y: 236
        width: 321
        height: 226
        delegate: Item {
            x: 5
            width: 80
            height: 40
            Row {
                Text {text: name}
                Text {text: " : "}
                Text {text: number}

            }
        }
        model: ListModel {
            id: cardListModel
            ListElement {
                name: "背心"
                //name: "back"
                number: "3"
            }
            ListElement {
                name: "胸罩"
                //name: "back"
                number: "5"
            }
        }
    }
    TextField {
        id: addCardNameTextField
        x: 373
        y: 114
        text: qsTr("Card Name")
    }

    TextField {
        id: addCardNumberTextField
        x: 596
        y: 114
        width: 98
        height: 40
        text: qsTr("Number")
    }
    Button {
        id: addCardButton
        x: 373
        y: 175
        width: 115
        height: 40
        text: qsTr("Add Card")
        onClicked: {
            cardListModel.append({name:addCardNameTextField.text, number:addCardNumberTextField.text})
        }
    }


    Button {
        id: submitUserInputButton
        x: 535
        y: 468
        width: 159
        height: 40
        text: qsTr("Submit")
        //i: 0
        onClicked: {
            var i
            for(i=0; i<shopListModel.count; i++) {
                submit.appendShop( shopListModel.get(i).shopLink );
            }
            for(i=0; i<cardListModel.count; i++) {
                submit.appendCard( cardListModel.get(i).name, cardListModel.get(i).number)
            }

            submit.clicked()
        }
    }
}
