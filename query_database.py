from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
import datetime

#from database_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///shelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
s = session.query(Puppy).all()

# 1. all puppies organized alphabetically
pupy_names = [n.name for n in s ]
pupy_names.sort()
for pupy  in pupy_names:
	print(pupy)

#2. pupies less than 6 months old by youngest first
# today = datetime.date.today()
# young_puppies = [ ]
# for p in s:
# 	age = today - p.dateOfBirth
# 	if age.days <= 180:
# 		young_puppies.append((age.days, p.name, p.id, p.shelter_id))
# young_puppies.sort()
# print(young_puppies)


