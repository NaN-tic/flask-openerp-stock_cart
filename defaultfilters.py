#This file is part openerp-stock-cart app for Flask.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import jinja2
from flask.ext.babel import Babel, gettext as _

def floatwithoutdecimal(text):
    """
    Convert a float to integer.

    * num1 = 34.23234
    * num2 = 34.00000
    * num3 = 34.26000
    * {{ num1|floatformat }} displays "34"
    * {{ num2|floatformat }} displays "34"
    * {{ num3|floatformat }} displays "34"
    """

    try:
        float(text)
    except:
        return ''

    return '{0:g}'.format(float(text))
jinja2.filters.FILTERS['floatwithoutdecimal'] = floatwithoutdecimal

def pickingname(pickings, arg):
    """
    Get picking name from dict.

    * pickings = {'1': {'name': 'P1230', 'products': []}
    """
    if not arg:
        return None
    return pickings[str(arg)]['name']
jinja2.filters.FILTERS['pickingname'] = pickingname

def pickingproducts(pickings, arg):
    """
    Get picking name from dict.

    * pickings = {'1': {'name': 'P1230', 'products': []}
    """
    if not arg:
        return None
    return pickings[str(arg)]['products']
jinja2.filters.FILTERS['pickingproducts'] = pickingproducts

def productinfo(product):
    """
    Get product dict values and return str html.
    """
    product_info = []
    if product.get('code'):
        product_info.append('%s: %s' % (_(u'Code'), product.get('code')))
    if product.get('ean13'):
        product_info.append('%s: %s' % (_(u'EAN13'), product.get('ean13')))
    if product.get('loc_rack'):
        product_info.append('%s: %s' % (_(u'Rack'), product.get('loc_rack')))
    if product.get('loc_row'):
        product_info.append('%s: %s' % (_(u'Row'), product.get('loc_row')))
    if product.get('loc_case'):
        product_info.append('%s: %s' % (_(u'Case'), product.get('loc_case')))
    if product.get('manufacturer'):
        product_info.append('%s: %s' % (_(u'Manufacturer'), product.get('manufacturer')))
    if product.get('location'):
        product_info.append('%s: %s' % (_(u'Location'), product.get('location')))
    return "<br/>".join(product_info)
jinja2.filters.FILTERS['productinfo'] = productinfo

def productmove(product):
    """
    Get move from dict.
    """
    return product.get('move')
jinja2.filters.FILTERS['productmove'] = productmove
