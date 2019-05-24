#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random, string

# Creates a flow object from the clientsecrets JSON file
# This JSON formatted style stores your client ID, client secret and
# other OAuth2.0 parameters
from oauth2client.client import flow_from_clientsecrets
# Use FlowExchangeError if we run into an error trying to exchange an
# authorization code for an access token.
from oauth2client.client import FlowExchangeError
import httplib2
import json
# It converts the return value from a function into a real response object
# that we can send off to our client
from flask import make_response
import requests

engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False}, echo=True)

#Connect to Database and create database session
# engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(9)
    return render_template('category.html', categories = categories, latest_items = latest_items)

@app.route('/catalog/category/new', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name = request.form['name'], user_id = "#####")
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
            return redirect(url_for('showCatalog'))
        else:
            return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')

@app.route('/catalog/category/<int:category_id>/edit')
def editCategory(category_id):
    return "Edit Category %s" % category_id

@app.route('/catalog/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return "Delete Category %s" % category_id

@app.route('/catalog/category/<int:category_id>/item')
def showItem(category_id):
    return "Show Items %s" % category_id

@app.route('/catalog/category/<int:category_id>/item/new')
def newItem(category_id):
    return "New Item %s" % category_id

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/edit')
def editItem(category_id, item_id):
    return "Edit Item %s %s" % (category_id, item_id)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return "Delete Item %s %s" % (category_id, item_id)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
