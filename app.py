#!/usr/bin/env Python 2.7.16rc1
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, desc, asc, and_, insert
from sqlalchemy.orm import sessionmaker
from dataBase_setup import Base, Categories, Items

app = Flask(__name__)

engine = create_engine('sqlite:///categoriesitem.db')
# engine = create_engine('postgresql://scott:tiger@localhost/categoriesitem')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    categories = session.query(Categories).all()
    items = session.query(Items.name, Categories.name).join(Categories).filter(Categories.id == Items.category_id).order_by(desc('items.id')).limit(9)
    print(items)
    return render_template('index.html', categories = categories, items = items)

@app.route('/catalog/<string:category_name>/items')
def showItems(category_name):
    if request.method == 'POST':
        print('post')
    else:
        categories = session.query(Categories).all()
        print(category_name)
        category_id = session.query(Items.name, Categories.name).join(Categories).filter_by(name=category_name)
        print(category_id)
        # items = session.query(Items.name).join(Categories).filter(Categories.id == Items.category_id)
        # print(items)
        return render_template('displayItems.html', categories = categories, cat = category_id)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def itemDetails(category_name, item_name):
    if request.method == 'POST':
        print('post')
    else:
        # item = session.query(Items).join(Categories).filter(Categories.name == category_name, Items.name == item_name)
        item = session.query(Items).join(Categories).filter(and_(Categories.name == category_name, Items.name == item_name))
        print(item)
        return render_template('itemDetails.html', item = item)


@app.route('/catalog/new', methods = ['GET', 'POST'])
def newItem():
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
        return redirect(url_for('index'))
    else:
        categories = session.query(Categories).all()
        return render_template('addItem.html', categories = categories)


@app.route('/catalog/<string:item_name>/edit', methods = ['GET', 'POST'])
def editItem(item_name):
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
        categories = session.query(Categories).all()
        return render_template('editItem.html', item = item, categories = categories)


@app.route('/catalog/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_name):
    itemToDelete = session.query(Categories.name, Items).join(Items).filter_by(name=item_name).one()
    print(itemToDelete)
    if request.method == 'POST':
        print(itemToDelete.Items)
        session.delete(itemToDelete.Items)
        session.commit()
        return redirect(url_for('showItems', category_name = itemToDelete.name))
    else:
        return render_template('deleteconfirmation.html', item = itemToDelete)

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
    app.run(host='0.0.0.0', port=5000)
