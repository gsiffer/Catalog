from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
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
User1 = User(name="Gabor Siffer", email="gabor.siffer@gmail.com",
             picture='')
session.add(User1)
session.commit()

category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

Item1 = Item(user_id=1, name="Soccer Ball", description="Description Soccer Ball",
                  category=category1)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Soccer Cleats", description="Description Soccer Cleats",
                  category=category1)

session.add(Item2)
session.commit()

category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()

Item1 = Item(user_id=1, name="Ball", description="Description Ball",
                  category=category2)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Hoop", description="Description Hoop",
                  category=category2)

session.add(Item2)
session.commit()

category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()

Item1 = Item(user_id=1, name="Baseball Gloves", description="Description Baseball Gloves",
                  category=category3)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Baseball Bat", description="Description Baseball Bat",
                  category=category3)

session.add(Item2)
session.commit()

category4 = Category(user_id=1, name="Frisbee")

session.add(category4)
session.commit()

Item1 = Item(user_id=1, name="Discs", description="Description Discs",
                  category=category4)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Shoes", description="Description Shoes",
                  category=category4)

session.add(Item2)
session.commit()

category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()

Item1 = Item(user_id=1, name="Goggles", description="Description Goggles",
                  category=category5)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Snowboard", description="Description Snowboard",
                  category=category5)

session.add(Item2)
session.commit()

category6 = Category(user_id=1, name="Rock Climbing")

session.add(category6)
session.commit()

Item1 = Item(user_id=1, name="Rope", description="Description Rope",
                  category=category6)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Helmet", description="Description Helmet",
                  category=category6)

session.add(Item2)
session.commit()

category7 = Category(user_id=1, name="Foosball")

session.add(category7)
session.commit()

Item1 = Item(user_id=1, name="Foosball Table", description="Description Foosball Table",
                  category=category7)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Foosball Ball", description="Description Foosball Ball",
                  category=category7)

session.add(Item2)
session.commit()

category8 = Category(user_id=1, name="Skating")

session.add(category8)
session.commit()

Item1 = Item(user_id=1, name="Skate", description="Description Skate",
                  category=category8)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Helmet", description="Description Helmet",
                  category=category8)

session.add(Item2)
session.commit()

category9 = Category(user_id=1, name="Hockey")

session.add(category9)
session.commit()

Item1 = Item(user_id=1, name="Hockey Skate", description="Description Hockey Skate",
                  category=category9)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Stick", description="Description Stick",
                  category=category9)

session.add(Item2)
session.commit()

print "added menu items!"
