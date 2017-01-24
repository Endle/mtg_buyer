from main import Item, TEMP_FOLDER
import logging

def resolve(item:Item):
    logging.warn("resolve " + item.card)


if __name__ == '__main__':
    i = Item()
    i.html = "beef"
    i.card = "文胸"
    with open("/Users/lizhenbo/Downloads/mtg/文胸") as fin:
        i.html = fin.read()
    resolve(i)
