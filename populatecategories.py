from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataBase_setup import Base, Categories, Items, Users

engine = create_engine('sqlite:///categoriesitemwithusers.db')
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

# Create dummy user
User1 = Users(name="Osumgba Chiamaka", email="osumgbachiamaka@gmail.com",
             picture='https://res.cloudinary.com/duxoxictr/image/upload/v1563888240/IMG_5704.jpg')
session.add(User1)
session.commit()

# Menu for Mammals
category1 = Categories(name="Mammals")

session.add(category1)
session.commit()
print(category1.id)


items1 = Items(name="Dog", category_id=1, description = 'The domestic dog (Canis lupus familiaris when considered a subspecies of the wolf or Canis familiaris when considered a distinct species) is a member of the genus Canis (canines), which forms part of the wolf-like canids, and is the most widely abundant terrestrial carnivore.')

session.add(items1)
session.commit()

category2 = Categories(name="Reptiles")
session.add(category2)
session.commit()
print(category2.id)

items1 = Items(name="Cat", category_id=category1.id, description = 'The cat is a small carnivorous mammal. It is the only domesticated species in the family Felidae and often referred to as the domestic cat to distinguish it from wild members of the family. The cat is either a house cat or a farm cat, which are pets, or a feral cat, which ranges freely and avoids human contact.')

session.add(items1)
session.commit()

items2 = Items(name="lizards", category_id=category2.id, description = 'Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica, as well as most oceanic island chain')

session.add(items2)
session.commit()

# items3 = Items(name="Chocolate Cake", category_id=category1)

# session.add(items3)
# session.commit()


print "added alot of items!"
