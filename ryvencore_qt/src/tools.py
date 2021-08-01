import enum
import json
import os
from math import sqrt

from .ryvencore.tools import serialize, deserialize


def pythagoras(a, b):
    return sqrt(a ** 2 + b ** 2)


def get_longest_line(s: str):
    lines = s.split('\n')
    lines = [line.replace('\n', '') for line in lines]
    longest_line_found = ''
    for line in lines:
        if len(line) > len(longest_line_found):
            longest_line_found = line
    return line


def shorten(s: str, max_chars: int, line_break: bool = False):
    """Ensures, that a given string does not exceed a given max length. If it would, its cut in the middle."""
    l = len(s)
    if l > max_chars:
        insert = ' . . . '
        if line_break:
            insert = '\n'+insert+'\n'
        insert_length = len(insert)
        left = s[:round((max_chars-insert_length)/2)]
        right = s[round(l-((max_chars-insert_length)/2)):]
        return left+insert+right
    else:
        return s


class MovementEnum(enum.Enum):
    # this should maybe get removed later
    mouse_clicked = 1
    position_changed = 2
    mouse_released = 3


def change_svg_color(filepath: str, color_hex: str):


    from qtpy.QtSvg import QSvgRenderer
    from qtpy.QtGui import QPixmap, QPainter
    from qtpy.QtCore import Qt

    with open(filepath) as f:
        data = f.read()
    data = data.replace('fill:#000000', 'fill:'+color_hex)
    with open(filepath, 'w') as f:
        f.write(data)

    svg_renderer = QSvgRenderer(filepath)
    pix = QPixmap(svg_renderer.defaultSize())
    pix.fill(Qt.transparent)
    pix_painter = QPainter(pix)
    svg_renderer.render(pix_painter)

    return pix



    # """
    # Changes the color of an SVG image and returns a QPixmap
    #
    # https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt
    # """
    #
    # from qtpy.QtGui import Qt, QPainter
    # from qtpy.QtXml import QDomDocument, QDomElement
    # from qtpy.QtSvg import QSvgRenderer
    # from qtpy.QtGui import QPixmap
    #
    #
    # def change_svg_color__set_attr_recur(elem: QDomElement, strtagname: str, strattr: str, strattrval: str):
    #
    #     # if it has the tag name then overwrite desired attribute
    #     if elem.tagName() == strtagname:
    #         elem.setAttribute(strattr, strattrval)
    #
    #     # loop all children
    #     for i in range(elem.childNodes().count()):
    #         if not elem.childNodes().at(i).isElement():
    #             continue
    #
    #         change_svg_color__set_attr_recur(elem.childNodes().at(i).toElement(), strtagname, strattr, strattrval)
    #
    #
    # # open svg resource load contents to qbytearray
    # f = open(filepath)
    # data = f.read()
    # f.close()
    # # load svg contents to xml document and edit contents
    # doc = QDomDocument()
    # doc.setContent(data)
    # # recursively change color
    # change_svg_color__set_attr_recur(doc.documentElement(), 'path', 'fill', color_hex)
    # # create svg renderer with edited contents
    # svg_renderer = QSvgRenderer(doc.toByteArray())
    # # create pixmap target (could be a QImage)
    # pix = QPixmap(svg_renderer.defaultSize())
    # pix.fill(Qt.transparent)
    # # create painter to act over pixmap
    # pix_painter = QPainter(pix)
    # # use renderer to render over painter which paints on pixmap
    # svg_renderer.render(pix_painter)
    #
    # return pix