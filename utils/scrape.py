"""Base scraping utils."""
import requests
import re

from lxml import etree, html


XML_NAMESPACE_ATTRS = r'xmlns\=\"[^\"]+\"|xmlns\:[a-z]+\=\"[^\"]+\"|(?<=\s)[a-z]+\:'


def element_tree(page, tree_type=None):
    """Convert an HTML or XML page into a parsed tree of elements."""
    # Do nothing.
    if hasattr(page, "xpath"):
        return page
    if hasattr(page, "tree"):
        return page.tree
    # If page is not a string, convert it
    if hasattr(page, "page_source"):
        page = page.page_source
    if isinstance(page, requests.models.Response):
        page = page.content

    if not tree_type:
        html_elems = html.fromstring(page).find('.//*')
        tree_type = "html" if html_elems is not None else "xml"

    if tree_type == "html":
        return html.fromstring(page)
    elif tree_type == "xml":
        page = re.sub(XML_NAMESPACE_ATTRS, "", page) # remove namespace attributes for simpler xpaths
        return etree.fromstring(page)

    raise TypeError("Tree type must be set as either html or xml!")


def value(page, xpath):
    """Scrapes a single value from the page.

    >>> title = scrape.value(page, '/head/title/text()')
    """
    tree = element_tree(page)

    elems = tree.xpath(xpath)
    return value_from_elements(elems)


def values(page, base_xpath, xpaths=None):
    """Scrapes a dictionary of name:values.

    >>> record = scrape.values(page, '//div[@id="info"]', {
    ...    'name': 'div[@class="name"]/text()',
    ...    'address': 'div[@class="address"]/a/text()',
    ...    'url': 'div[@class="url"]/a/@href',
    ... })
    """
    tree = element_tree(page)

    if not xpaths: # allow for no `base_xpath` arg
        xpaths, base_xpath = base_xpath, xpaths

    if base_xpath:
        base_elems = tree.xpath(base_xpath)
        if not base_elems:
            return {}
        tree = base_elems[0]
    return { name: value(tree, xpath) for name, xpath in xpaths.items() }


def rows(page, xpath, column_xpaths):
    """Scrapes rows of data, such as off of a table.

    >>> records = scrape.rows(page, '//table[1]/tbody/tr', {
    ...    'table_column_1': 'td[1]/text()',
    ...    'table_column_2': 'td[2]/a/text()',
    ...    'table_column_2_link': 'td[2]/a/@href',
    ... })
    """
    tree = element_tree(page)
    return [values(row, column_xpaths) for row in tree.xpath(xpath)]


def value_from_elements(elems):
    """Takes node elements and concatenates their inner text to a single value."""
    def to_value(elem):
        if isinstance(elem, str):
            return str(elem).strip()
        return u''.join(elem.itertext())

    if len(elems) == 1:
        return to_value(elems[0])
    elif len(elems) == 0:
        return u''
    else:
        values = filter(lambda val: not val, [to_value(elem) for elem in elems])
        if isinstance(values, list) and len(values) == 1:
            values = values[0]
        return list(values)
