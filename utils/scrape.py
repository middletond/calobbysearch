import requests
import re

from lxml import etree
from lxml import html


XML_NAMESPACE_ATTRS = r'xmlns\=\"[^\"]+\"|xmlns\:[a-z]+\=\"[^\"]+\"|(?<=\s)[a-z]+\:'


def tree_from_page(page, tree_type=None):
    """Convert an HTML or XML page into a parsed tree."""
    if hasattr(page, "tree"):
        return page.tree
    else:
        if hasattr(page, "page_source"): # web page
            page = page.page_source
        if isinstance(page, requests.models.Response): # requests object
            page = page.text

    if not tree_type:
        html_elems = html.fromstring(page).find('.//*')
        tree_type = "html" if html_elems is not None else "xml"

    if tree_type == "html":
        return html.fromstring(page)
    elif tree_type == "xml":
        page = re.sub(XML_NAMESPACE_ATTRS, "", page) # remove namespace attributes for simpler xpaths
        return etree.fromstring(page)

    raise TypeError("Tree type must be set as either html or xml!")


def rows(page, xpath, column_xpaths):
    """Scrapes rows of data, such as off of a table.

    >>> records = scrape.rows(browser, '//table[1]/tbody/tr', {
    ...    'table_column_1': 'td[1]/text()',
    ...    'table_column_2': 'td[2]/a/text()',
    ...    'table_column_2_link': 'td[2]/a/@href',
    ... })

    Args:
        xpath (str): The xpath that matches each record.
        column_xpaths (dict): The dictionary of xpaths for each record.
    """
    tree = tree_from_page(page)

    records = []
    for row in tree.xpath(xpath):
        record = {}
        for column_name in column_xpaths.keys():
            value_elements = row.xpath(column_xpaths[column_name])
            record[column_name] = value_from_elements(value_elements)
        records.append(record)
    return records


def values(page, base_xpath, xpaths=None):
    """Scrapes a dictionary of values.

    xpaths (dict): The dictionary of xpaths. This is used in the same way that
        :func:`.rows` uses it, except it's only used once.
    base_xpath (str): An optional xpath whose corresponding element is used as a
        base for the xpaths in the dictionary.
    """
    if xpaths is None:
        xpaths, base_xpath = base_xpath, xpaths

    tree = tree_from_page(page)
    if base_xpath is not None:
        base = tree.xpath(base_xpath)
        if not base:
            return {} # no base matches so no values either
        else:
            base = base[0]
    else:
        base = tree

    value_dict = {}
    for name, xpath in xpaths.items():
        value_dict[name] = value_from_elements(base.xpath(xpath))
    return value_dict


def value(page, xpath):
    """Scrapes a single value from the page.

    >>> title = scrape.value(browser, '/head/title/text()')
    """
    tree = tree_from_page(page)

    value_elements = tree.xpath(xpath)
    return value_from_elements(value_elements)


def form_values(page, fieldnames):
    """Scrape form values from a page by field name."""
    return {name: value(page, '//input[@name="{}"]/@value'.format(name)) for name in fieldnames}


def value_from_elements(elems):
    """Takes node elements and concatenates their inner text to a single value."""
    def to_value(elem):
        if isinstance(elem, str):
            return str(elem).strip()
        else:
            return ''.join(elem.itertext())

    if len(elems) == 1:
        return to_value(elems[0])
    elif len(elems) == 0:
        return u''
    else:
        values = filter(lambda val: not val, [to_value(elem) for elem in elems])
        if isinstance(values, list) and len(values) == 1:
            values = values[0]
        return list(values)
