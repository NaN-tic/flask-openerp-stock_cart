#This file is part openerp-stock-cart app for Flask.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import os
import ConfigParser
import erppeek
import bz2
import socket
from functools import wraps

from flask import Flask, render_template, request, jsonify, abort, session, redirect, url_for, flash
from flask.ext.babel import Babel, gettext as _

from apphelp import get_description
from form import *
from defaultfilters import *


def get_config():
    '''Get values from cfg file'''
    conf_file = '%s/config.ini' % os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    results = {}
    for section in config.sections():
        results[section] = {}
        for option in config.options(section):
            results[section][option] = config.get(section, option)
    return results

def create_app(config=None):
    '''Create Flask APP'''
    cfg = get_config()
    app_name = cfg['flask']['app_name']
    app = Flask(app_name)
    app.config.from_pyfile(config)

    return app

def get_template(tpl):
    '''Get template'''
    return "%s/%s" % (app.config.get('TEMPLATE'), tpl)

def parse_setup(filename):
    globalsdict = {}  # put predefined things here
    localsdict = {}  # will be populated by executed script
    execfile(filename, globalsdict, localsdict)
    return localsdict

def get_lang():
    return app.config.get('LANGUAGE')

def erp_connect():
    '''OpenERP Connection'''
    server = app.config.get('OPENERP_SERVER')
    database = app.config.get('OPENERP_DATABASE')
    username = session['username']
    password = bz2.decompress(session['password'])
    try:
        Client = erppeek.Client(server, db=database, user=username, password=password)
    except socket.error:
        flash(_("Can't connect to ERP server. Check network-ports or ERP server was running."))
        abort(500)
    except:
        abort(500)
    return Client

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged = session.get('logged_in', None)
        if not logged:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


conf_file = '%s/config.cfg' % os.path.dirname(os.path.realpath(__file__))
app = create_app(conf_file)
app.config['BABEL_DEFAULT_LOCALE'] = get_lang()
app.root_path = os.path.dirname(os.path.abspath(__file__))
babel = Babel(app)

# OpenERP models - access
MODELS_ACCESS = ({
    'stock.picking': 'write',
    'stock.cart': 'read',
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template(get_template('404.html')), 404

@app.errorhandler(500)
def server_error(e):
    return render_template(get_template('500.html')), 500

@app.route('/')
@login_required
def index():
    '''Dashboard'''
    cart = session.get('cart', None)
    if not cart:
        return redirect(url_for('cart'))

    return render_template(get_template('index.html'))

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Login'''
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = bz2.compress(request.form.get('password'))
        session['username'] = username
        session['password'] = password

        Client = erp_connect()
        login = Client.login(username, bz2.decompress(password), app.config.get('OPENERP_DATABASE'))
        if login:
            access = True
            for key, value in MODELS_ACCESS.iteritems():
                if not Client.access(key, mode=value):
                    access = False
                    flash(_('Error: Not access in %(key)s - %(value)s' % { 'key': key, 'value': value} ))
            if access:
                session['logged_in'] = True
                flash(_('You were logged in.'))
                return redirect(url_for('index'))
        else:
            flash(_('Error: Invalid username or password'))

    return render_template(get_template('login.html'), form=form)

@app.route('/logout')
def logout():
    '''Logout App'''
    Client = erp_connect()

    # Remove all stock.cart by user
    StockCart = Client.model('stock.cart')
    user_id = Client.search('res.users',[
                ('login', '=', session.get('username')),
                ])[0]
    carts = Client.search('stock.cart',[
                ('user_id', '=', user_id),
                ])
    for cart in carts:
        c = StockCart.get(cart)
        c.write({'user_id': None})

    # Remove all sessions
    session.pop('logged_in', None)

    session.pop('username', None)
    session.pop('password', None)
    session.pop('cart', None)
    session.pop('cart_name', None)

    flash(_('You were logged out.'))
    return redirect(url_for('login'))

@app.route('/cart', methods=["GET"])
@login_required
def cart():
    '''Select a stock cart by user'''
    Client = erp_connect()
    StockCart = Client.model('stock.cart')

    '''Drop currenty cart by user'''
    if session.get('cart'):
        cart_old = StockCart.get(int(session.get('cart')))
        cart_old.write({'user_id': None})
        session.pop('cart', None)
        session.pop('cart_name', None)

    '''Get cart id and add who working in stock.cart'''
    if request.method == 'GET':
        cart = request.args.get('cart', None)
        order = request.args.get('order', None)

        if cart:
            try:
                # Get Cart object from request.get
                id = int(cart)
                cart = StockCart.get(id)

                if not cart.user_id and cart.active:
                    #get user id
                    user_id = Client.search('res.users',[
                                ('login', '=', session.get('username')),
                                ])[0]

                    # Add new session values and log in stock.cart
                    session['cart'] = cart.id
                    session['cart_name'] = cart.name
                    session['cart_rows'] = cart.rows
                    session['cart_columns'] = cart.columns

                    cart.write({'user_id': user_id})
                    return redirect(url_for('index'))
                else:
                    if cart.user_id:
                        flash(_(u'Cart %(name)s is working by user %(user)s.', name=cart.name, user=cart.user_id))
                    else:
                        flash(_(u'Not find some cart by %(id)s.', id=cart))
            except:
                flash(_('Error: Cart ID not valid or empty'))

        if order:
            flash(_(u'Order products by: %(order)s.', order=order))
            session['order'] = order
    
    carts = StockCart.browse([('active', '=', True)])
    return render_template(get_template('cart.html'), carts=carts)

@app.route('/picking')
@login_required
def picking():
    '''Get all pickings and get info to make pickings'''
    cart = session.get('cart', None)
    order = session.get('order', None)
    if not cart:
        return redirect(url_for('cart'))

    Client = erp_connect()
    products, picking_grid = Client.execute('stock.picking', 'get_products_to_cart', cart, order)

    return render_template(get_template('picking.html'), products=products, grid=picking_grid)

@app.route('/basket', methods=['PUT', 'POST'])
def basket():
    '''
    Process values from form basket
    name: picking-product ID's
    value: qty to add in basket
    '''
    cart = session.get('cart', None)
    Client = erp_connect()

    values = []
    result = True
    for data in request.json:

        try:
            move = int(data['name'])
            qty = int(data['value'])
        except:
            result = False

        values.append({
            'move': move,
            'qty': qty,
            })

    if result:
        Client.execute('stock.picking', 'set_products_to_cart', cart, values)

    return jsonify(result=result)

@app.route('/help')
def help():
    '''Help - Documentation'''
    lang = get_lang()
    description = get_description(lang)
    return render_template(get_template('help.html'), content=description)

if __name__ == "__main__":
    app.run()
