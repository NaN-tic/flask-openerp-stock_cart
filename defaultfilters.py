#This file is part openerp-stock-cart app for Flask.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import jinja2

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

    * pickings = {'1': 'P1230', '2': 'P1231'}
    """
    if not arg:
        return None
    return pickings[str(arg)]
jinja2.filters.FILTERS['pickingname'] = pickingname
