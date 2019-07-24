from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataBase_setup import Base, Categories, Items

engine = create_engine('sqlite:///categoriesitem.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
# category1 = Categories(name="Soccer")

# session.add(category1)
# session.commit()
# print(category1.id)


items1 = Items(name="hocky", category_id=1, description = 'hoc1 kjknjkknz jnjzt')

session.add(items1)
session.commit()


# items1 = Items(name="soc", category_id=category1.id, description = 'soc, soc, soc, soc, soc, soc, soc')

# session.add(items1)
# session.commit()

# items1 = Items(name="Chicken Balls", category_id=category1.id, description = 'A very nice bat, with a very spacious  bla bla bla bla. A very nice chicken ball, ')

# session.add(items1)
# session.commit()

# items3 = Items(name="Chocolate Cake", category_id=category1)

# session.add(items3)
# session.commit()


print "added alot of items!"
