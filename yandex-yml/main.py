from xml.etree import ElementTree as etree
import csv

yml_stub = """
<yml_catalog date="{date}">
  <shop>
    <name>{name}</name>
    <company>{company}</company>
    <url>{url}</url>
    <currencies>
      <currency id="RUR" rate="1"/>
    </currencies>
    <categories>
    </categories>
    <offers>
    </offers>
  </shop>
</yml_catalog>
"""
csv_fname = '../practica_price.csv'
yml_fname = '../pricelist.yml'


def insert_categories(node, categories):
    for cat in categories:
        etree.SubElement(node, 'category', id=categories[cat]).text = cat


def new_from_stub(data, stub):
    return etree.fromstringlist(
        [l.strip() for l in stub.format(**data).splitlines()]
    )


def write_tree(tree, fname=yml_fname):
    tree.write(fname, encoding='utf-8', xml_declaration=True)


def price_date():
    from datetime import datetime
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")


def offer_from_dic(dic):
    attrs = ('id', 'type', 'available')
    el = etree.Element('offer', **{k: dic[k] for k in dic if k in attrs})
    for k in {k: dic[k] for k in dic if k not in attrs}:
        etree.SubElement(el, k).text = dic[k]
    return el


def insert_offers(offers_node, price):
    for item in price:
        offers_node.append(offer_from_dic(item))


def practica_book(book, categories):
    for k in book:
        if k == 'category':
            yield 'categoryId', categories[book[k]]
        elif k in ('delivery'):
            continue
        else:
            yield k, book[k]


def parse_practica_price(price_reader, categories):
    return ({k: v for k, v in practica_book(book, categories)}
            for book in price_reader)


def practica_categories(price_reader):
    return {book['category']: str(id(book['category']))
            for book in price_reader}


def pretty_print(fname=yml_fname):
    from lxml import etree as lxml_etree
    lxml_etree.parse(fname).write(
        fname, xml_declaration=True, encoding='utf-8', pretty_print=True)


def main(price_fname=csv_fname):
    data = dict(
        name="ИД Практика",
        company="ООО Издательский дом Практика",
        url="http://practica.ru",
        date=price_date(),
    )
    root = new_from_stub(data, yml_stub)
    shop = root.find('shop')
    categories_node = shop.find("categories")
    offers_node = shop.find("offers")

    with open(price_fname) as f:
        price = csv.DictReader(f, dialect='excel')
        categories = practica_categories(price)
        insert_categories(categories_node, categories)
        f.seek(0)
        price = csv.DictReader(f, dialect='excel')
        insert_offers(offers_node, parse_practica_price(price, categories))

    tree = etree.ElementTree(root)
    write_tree(tree)
    pretty_print()

main()
