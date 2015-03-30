from sqlalchemy import Integer, String, Column, Float, Boolean, Text, Unicode, Time, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA

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
    category = Column('category', String(500))
    predicted_topic_50 = Column('predicted_topic_50', Text())
    predicted_topic_22 = Column('predicted_topic_22', Text())
    svm_model_topic_22 = Column('svm_model_topic_22', BYTEA())
    svm_model_topic_50 = Column('svm_model_topic_50', BYTEA())

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


class User(Base):
    __tablename__ = 'yelp_user'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(22), unique=True, index=True)
    user_type= Column('type', String(10))
    name = Column('name', String(200))
    review_count = Column('review_count', Integer)
    average_stars = Column('average_stars', Float(precision=6))
    yelping_since = Column('yelping_since', String(20))
    compliments = Column('compliments', String(2000))
    votes = Column('votes', String(200))
    elite = Column('elite', String(200))
    predicted_topic_50 = Column('predicted_topic_50', Text())
    predicted_topic_22 = Column('predicted_topic_22', Text())
    svm_model_topic_22 = Column('svm_model_topic_22', BYTEA())
    svm_model_topic_50 = Column('svm_model_topic_50', BYTEA())

    def __repr__(self):
        return "<User(user_id='%s', name='%s', review_count='%d', average_stars='%f', yelping_since='%s')>" % (
                self.user_id,
                self.name,
                self.review_count,
                self.average_stars,
                self.yelping_since
                )


class Friendship(Base):
    __tablename__ = 'friendship'

    user1 = Column('user1', String(22), primary_key=True)
    user2 = Column('user2', String(22), primary_key=True)


class Tip(Base):
    __tablename__ = 'tip'

    business_id = Column('business_id', String(22), primary_key=True)
    user_id = Column('user_id', String(22), primary_key=True)
    text = Column('text', Text())
    likes = Column('likes', Integer)
    date = Column('date', Date())
    tip_type = Column('type', String(3))


class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column('id', Integer)
    name = Column('name', String(200), primary_key=True)
    value = Column('value', String(2000), primary_key=True)


class BusinessAttribute(Base):
    __tablename__ = 'business_attribute'

    attribute_id = Column('attribute_id', Integer, primary_key=True)
    business_id = Column('business_id', Integer)
    business_bid = Column('business_bid', String(22), primary_key=True)


class Review(Base):
    __tablename__ = 'review'

    review_id = Column('review_id', String(22), primary_key=True)
    user_id = Column('user_id', String(22))
    business_id = Column('business_id', String(22))
    date = Column('date', Date())
    stars = Column('stars', Integer)
    text = Column('text', Text())
    tags = Column('tags', Text())
    words = Column('words', Text())
    review_type = Column('type', String(6))
    predicted_topic_50 = Column('predicted_topic_50', Text())
    predicted_topic_22 = Column('predicted_topic_22', Text())


class ReviewVote(Base):
    __tablename__ = 'review_vote'

    review_id = Column('review_id', String(22), primary_key=True)
    vote = Column('vote', String(22), primary_key=True)
    number = Column('number', Integer)


class UserVote(Base):
    __tablename__ = 'user_vote'

    user_id = Column('user_id', String(22), primary_key=True)
    vote = Column('vote', String(22), primary_key=True)
    number = Column('number', Integer)

class BusinessTopic22(Base):
    __tablename__ = 'business_topic22'

    business_id = Column('business_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class BusinessTopic50(Base):
    __tablename__ = 'business_topic50'

    business_id = Column('business_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class ReviewTopic22(Base):
    __tablename__ = 'review_topic22'

    review_id = Column('review_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class ReviewTopic50(Base):
    __tablename__ = 'review_topic50'

    review_id = Column('review_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class UserTopic22(Base):
    __tablename__ = 'user_topic22'

    user_id = Column('user_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class UserTopic50(Base):
    __tablename__ = 'user_topic50'

    user_id = Column('user_id', String(22), primary_key=True)
    topic_id = Column('topic_id', Integer, primary_key=True)
    relationship = Column('relationship', Float(precision=20))
    stars = Column('stars', Float(precision=1))

class UserBusiness(Base):
    __tablename__ = 'user_business'

    user_id = Column('user_id', String(22), primary_key=True)
    business_id = Column('business_id', String(22), primary_key=True)
    stars = Column('stars', Float(precision=20))

class UserCategory(Base):
    __tablename__ = 'user_category'

    user_id = Column('user_id', String(22), primary_key=True)
    category_id = Column('category_id', Integer, primary_key=True)
    stars = Column('stars', Float(precision=1))
    relationship = Column('relationship', Float(precision=20))

class DetailedAttribute(Base):
    __tablename__ = 'detailed_attribute'

    id = Column('id', Integer, primary_key=True)
    parent_id = Column('parent_id', Integer)
    name = Column('name', String)

class BusinessDetailedAttribute(Base):
    __tablename__ = 'business_detailed_attribute'

    attribute_id = Column('attribute_id', Integer, primary_key=True)
    business_id = Column('business_id', String(22), primary_key=True)
    stars = Column('stars', Float(precision=1))
    raw_value = Column('raw_value', String)
    value = Column('value', Integer)
