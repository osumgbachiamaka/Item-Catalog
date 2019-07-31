#!/usr/bin/env Python 2.7.16rc1
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, desc, asc, and_, insert
from sqlalchemy.orm import sessionmaker
from dataBase_setup import Base, Categories, Items

# New imports for this step
from flask import session as login_session
import random, string

#import fot google authentication
from apiclient import discovery
import httplib2
from oauth2client import client
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog Application"

engine = create_engine('sqlite:///categoriesitem.db')
# engine = create_engine('postgresql://scott:tiger@localhost/categoriesitem')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#validating login
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)
    # # Set path to the Web application client_secret_*.json file you downloaded from the
    # # Google API Console: https://console.developers.google.com/apis/credentials
    # CLIENT_SECRET_FILE = '/path/to/client_secrets.json'
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = client.flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except client.FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

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

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print(login_session)
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
    

@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
#end of google login validation


@app.route('/')
@app.route('/catalog/')
def index():
    categories = session.query(Categories.id, Categories.name)
    items = session.query(Items.name, Categories.name).join(Categories).filter(Categories.id == Items.category_id).order_by(desc('items.id'))
    print(categories)
    # print(items)
    return render_template('index.html', categories = categories, items = items, login=login_session)

@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    if request.method == 'POST':
        print('post')
    else:
        categories = session.query(Categories)
        print(category_name)
        category_id = session.query(Items.name, Categories.name).join(Categories).filter_by(name=category_name)
        print(category_id)
        # items = session.query(Items.name).join(Categories).filter(Categories.id == Items.category_id)
        # print(items)
        return render_template('displayItems.html', categories = categories, cat = category_id, login=login_session)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def itemDetails(category_name, item_name):
    if request.method == 'POST':
        print('post')
    else:
        categories = session.query(Categories)
        # item = session.query(Items).join(Categories).filter(Categories.name == category_name, Items.name == item_name)
        item = session.query(Items).join(Categories).filter(and_(Categories.name == category_name, Items.name == item_name))
        print(item)
        return render_template('itemDetails.html', categories = categories, item = item, login=login_session)


@app.route('/catalog/new', methods = ['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        sel = session.query(Categories.id).filter_by(name = request.form['category'])
        print(sel)
        # sel = select([table1.c.a, table1.c.b]).where(table1.c.c > 5)
        # ins = table2.insert().from_select(['a', 'b'], sel)
        newItem = Items(name = request.form['item'], description = request.form['description'], category_id = sel)
        session.add(newItem)
        session.commit()
        # newItem = Items.insert().from_select(['category_id'], sel)
        print(newItem)
        return redirect(url_for('index', login=login_session))
    else:
        categories = session.query(Categories)
        return render_template('addItem.html', categories = categories, login=login_session)


@app.route('/catalog/<string:item_name>/edit', methods = ['GET', 'POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        # category_id = session.query(Categories.id).filter_by(name = request.form['category'])
        updateItem = session.query(Items).filter_by(id = request.form['id']).one()
        if request.form['title']:
            updateItem.name = request.form['title']
        if request.form['description']:
            updateItem.description = request.form['description']
        # updateItem = Items(name = request.form['title'], description = request.form['description'], category_id = category_id).filter_by(request.form['id'])
        print(updateItem)
        session.add(updateItem)
        session.commit()
        return redirect(url_for('itemDetails', category_name = request.form['category'], item_name = request.form['title']))
    else:
        # item = session.query(Items).join(Categories).filter(Categories.name == category_name, Items.name == item_name)
        item = session.query(Categories.name, Items).join(Items).filter(Items.name == item_name).one()
        print(item)
        categories = session.query(Categories)
        return render_template('editItem.html', item = item, categories = categories, login=login_session)


@app.route('/catalog/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    itemToDelete = session.query(Categories.name, Items).join(Items).filter_by(name=item_name).one()
    print(itemToDelete)
    categories = session.query(Categories)
    if request.method == 'POST':
        print(itemToDelete.Items)
        session.delete(itemToDelete.Items)
        session.commit()
        return redirect(url_for('showItems', category_name = itemToDelete.name))
    else:
        return render_template('deleteconfirmation.html', item = itemToDelete, categories = categories, login=login_session)

# JSON Endpoints
# Return JSON of all the categories in the catalog.
@app.route('/categories/catalog.json')
def show_category_catalog_json():
    """Return JSON of all the items in the catalog."""

    categories = session.query(Categories).order_by(Categories.id).all()
    return jsonify(Categories=[c.serialize for c in categories])


# Return JSON of all the items in the catalog.
@app.route('/items/catalog.json')
def show_item_catalog_json():
    """Return JSON of all the items in the catalog."""

    items = session.query(Items).order_by(Items.category_id.asc())
    return jsonify(Items=[i.serialize for i in items])

# Return JSON of a particular item in the catalog.
@app.route(
    '/catalog/<string:category_name>/<string:item_name>/JSON')
def catalog_item_json(category_name, item_name):
    """Return JSON of a particular item in the catalog."""

    item = session.query(Items)\
            .filter_by(name = item_name).all()

    if item is not None:
        return jsonify(item = [i.serialize for i in item])
    else:
        return jsonify(
            error='item {} does not belong to category {}.'
            .format(item_name, category_name))

        # return jsonify(error='The item or the category does not exist.')


@app.route('/catalog/<string:category_name>/JSON')
def categoryItemsJson(category_name):
    category = session.query(Categories).filter_by(id=1).one()
    # print(category.item)
    ite = session.query(Items).all()
    cat = session.query(Categories).all()
    # print(ite.categories)
    test=[]
    testItems=[]
    for c in cat:
        test.append(c)
        for i in ite:
            if (c.id == i.id):
                testItems.append(i)
            test.append(testItems)
        # test.append(i)
    print(test)
    return jsonify(Items=[c.serialize for c in test])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
