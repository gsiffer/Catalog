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



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
