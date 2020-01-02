# -*- coding: utf-8 -*-

"""Web handler for store related pages."""

import json

from flask import Blueprint, render_template, redirect, request, url_for

from models.store import Store
from models.user.decorators import requires_admin, requires_login

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
@requires_login
def index():
    """Shows all saved stores."""
    stores = Store.fetch_all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def new():
    """Adds a new store."""
    if request.method == 'POST':
        name = request.form['store-name']
        domain = request.form['store-domain']
        tag = request.form['item-tag']
        query = json.loads(request.form['item-query'])

        Store(name, domain, tag, query).save_to_db()

        return redirect(url_for('.index'))

    return render_template('stores/new.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def update(store_id: str):
    """Updates an existing store."""
    store = Store.fetch_by_id(store_id)

    if request.method == 'POST':
        name = request.form['store-name']
        domain = request.form['store-domain']
        tag = request.form['item-tag']
        query = json.loads(request.form['item-query'])

        store.name = name
        store.domain = domain
        store.html_tag_name = tag
        store.html_tag_attributes = query

        store.save_to_db()

        return redirect(url_for('.index'))

    return render_template('stores/edit.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete(store_id: str):
    """Deletes an existing store."""
    Store.fetch_by_id(store_id).delete()
    return redirect(url_for('.index'))
