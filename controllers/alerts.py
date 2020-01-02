# -*- coding: utf-8 -*-

"""Web handler for alert related pages."""

from flask import Blueprint, redirect, render_template, request, session, url_for

from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user.decorators import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@requires_login
def index():
    """Displays all saved alerts."""
    alerts = Alert.find_many('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new():
    """Adds a new alert."""
    if request.method == 'POST':
        item_name = request.form['item-name']
        item_url = request.form['item-url']
        price_limit = float(request.form['price-limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.html_tag_name, store.html_tag_attributes)
        item.fetch_price()
        item.save_to_db()

        alert = Alert(item_name, item._id, price_limit, session['email'])
        alert.save_to_db()

        return redirect(url_for('.index'))

    return render_template('alerts/new.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def update(alert_id: str):
    """Updates an existing alert."""
    alert = Alert.fetch_by_id(alert_id)

    if request.method == 'POST':
        alert.price_floor = float(request.form['price-limit'])
        alert.save_to_db()
        return redirect(url_for('.index'))

    return render_template('alerts/edit.html', alert=alert)


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete(alert_id: str):
    """Deletes an existing alert."""
    alert = Alert.fetch_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.delete()

    return redirect(url_for('.index'))
