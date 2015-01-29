from sqlalchemy import Integer, String, Column, Float, Boolean, Text, Unicode

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Business(Base):
    __tablename__ = 'business'

    id = Column('id', Integer, primary_key=True)
    business_id = Column('business_id', String(50))
    name = Column('name', Unicode(50))
    neighborhoods = Column('neighborhoods', String(200))
    full_address = Column('full_address', String(200))
    city = Column('city', String(200))
    state = Column('state', String(2))
    latitude = Column('latitude', Float(precision=6))
    longitude = Column('longitude', Float(precision=6))
    stars = Column('stars', Float(precision=1))
    review_count = Column('review_count', Integer)
    open_status = Column('open', Boolean)
    hours = Column('hours', String(500))
    attributes = Column('attributes', Text())
    business_type = Column('type', String(50))

    def __repr__(self):
        return "<Business(business_id='%s', name='%s', city='%s', state='%s', stars='%f', review_count='%d', hours='%s', attributes='%s', type='%s')>" % (
                self.business_id,
                self.name,
                self.city,
                self.state,
                self.stars,
                self.review_count,
                self.hours,
                self.attributes,
                self.business_type)


class Category(Base):
    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))

    def __repr__(self):
        return "<Category(id='%s', name='%s')>" % (
                self.id,
                self.name)

class BusinessCategory(Base):
    __tablename__ = 'business_category'

    category_id = Column('category_id', Integer, primary_key=True)
    business_id = Column('business_id', Integer, primary_key=True)
