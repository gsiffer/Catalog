#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# from sqlalchemy.ext.declarative import declarative_base

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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False}, echo=True)

#Connect to Database and create database session
# engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # print CLIENT_ID
    return render_template('login.html', STATE=state, client_id = CLIENT_ID)  #" The current session state is %s" %login_session['state']

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # print "wwwwwwwwwwwwwww %s" % login_session
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    # url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token'])
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json() # json.loads(answer.text)
    # print "wwwwwwwwwwwwwww %s" % data
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print ("done!")
    print ('access token is %s' % access_token)
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s' % access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # print'disconnect'
        # return response
        flash('You are successfully signed out.')
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/catalog/json')
def catalogJson():
    categories = session.query(Category).all()
    return jsonify(Category= [r.serialize for r in categories])

@app.route('/catalog/category/<int:category_id>/item/json')
def itemsJson(category_id):
    items = session.query(Item).filter_by(category_id = category_id)
    return jsonify(Item= [r.serialize for r in items])

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/description/json')
def itemJson(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return jsonify(Item= item.serialize)

@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(9)
    if 'username' not in login_session:
        return render_template('publicCategory.html', categories = categories,
            latest_items = latest_items)
    else:
        return render_template('category.html', categories = categories,
            latest_items = latest_items)

@app.route('/catalog/category/new', methods=['GET','POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            try:
                isExist = session.query(Category).filter_by(name =
                    request.form['name']).one()
            except:
                newCategory = Category(name = request.form['name'], user_id = login_session['user_id'])
                session.add(newCategory)
                flash('New Category %s Successfully Created' % newCategory.name)
                session.commit()
                return redirect(url_for('showItem', category_id = newCategory.id))
            flash('The "%s" category already exist' % isExist.name)
            return redirect(url_for('showItem', category_id = isExist.id))
        else:
            return redirect(url_for('newCategory'))
    else:
        return render_template('newCategory.html')

@app.route('/catalog/category/<int:category_id>/edit', methods = ['GET','POST'])
def editCategory(category_id):
  if 'username' not in login_session:
      return redirect('/login')
  editedCategory = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      if request.form['name']:
          try:
              isExist = session.query(Category).filter_by(name =
                  request.form['name']).one()
          except:
              editedCategory.name = request.form['name']
              session.commit()
              flash('Category Successfully Edited')
              return redirect(url_for('showItem', category_id = category_id))
          # flash('The "%s" category already exist' % isExist.name)
          return redirect(url_for('editCategory', category_id = category_id))
      else:
           return redirect(url_for('editCategory', category_id = category_id))
  else:
        return render_template('editCategory.html', editedCategory = editedCategory)

@app.route('/catalog/category/<int:category_id>/delete',
    methods = ['GET','POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        itemsToDelete = session.query(Item).filter_by(category_id = categoryToDelete.id).all()
        for item in itemsToDelete:
            session.delete(item)
            session.commit()
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        record = session.query(Category).order_by(asc(Category.name)).first()
        return redirect(url_for('showItem', category_id = record.id))
    else:
        return render_template('deleteCategory.html', categoryToDelete =
            categoryToDelete)

@app.route('/catalog/category/<int:category_id>/item')
def showItem(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    categoryOne = session.query(Category).filter_by(id = category_id).one()
    creator = getUserInfo(categoryOne.user_id)
    items = session.query(Item).filter_by(category_id = category_id ).all()
    if 'username' not in login_session:
        return render_template('publicItem.html', items =items, categories = categories,
            categoryOne = categoryOne, creator = creator)
    elif creator.id != login_session['user_id']:
        return render_template('publicItemUser.html', items =items, categories = categories,
            categoryOne = categoryOne, creator = creator)
    else:
        return render_template('item.html', items = items, categories = categories,
            categoryOne = categoryOne, creator = creator)

@app.route('/catalog/category/<int:category_id>/item/new', methods=['GET','POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            newItem = Item(name = request.form['name'], description =
            request.form['description'], category_id = category_id,
                user_id = category.user_id)
            session.add(newItem)
            session.commit()
            flash('New Item "%s" Successfully Created' % (newItem.name))
            return redirect(url_for('showItem', category_id = category_id))
        else:
            return redirect(url_for('newItem', category_id = category_id))
    else:
        return render_template('newItem.html', category = category)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id = item_id).one()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            session.commit()
            flash('Item Successfully Edited')
            return redirect(url_for('showItem', category_id = category_id))
        else:
            return redirect(url_for('editItem', category_id = category_id, item_id = item_id))
    else:
        return render_template('editItem.html', category = category, editedItem = editedItem )

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Item).filter_by(id = item_id).one()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItem', category_id = category_id))
    else:
        return render_template('deleteItem.html', category = category, deletedItem = deletedItem)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/description')
def description(category_id, item_id):
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(Item).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicDescription.html', category = category, item = item)
    else:
        return render_template('itemDescription.html', category = category, item = item)

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUser(login_session):
    newUser = User(name = login_session['username'], email =
        login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

# @app.route('/disconnect')
# def disconnect():
#     if 'provider' in login_session:
#         if login_session['provider'] == 'google':
#             gdisconnect()
#             del login_session['gplus_id']
#             del login_session['access_token']
#         if login_session['provider'] == 'facebook':
#             fbdisconnect()
#             del login_session['facebook_id']
#         del login_session['username']
#         del login_session['email']
#         del login_session['picture']
#         del login_session['user_id']
#         del login_session['provider']
#         flash("You have successfully been logged out.")
#         return redirect(url_for('showRestaurants'))
#     else:
#         flash("You were not logged in")
#         return redirect(url_for('showRestaurants'))



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
