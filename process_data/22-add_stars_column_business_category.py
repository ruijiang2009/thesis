from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Business, BusinessCategory

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

session = get_session()

business_categories = session.query(BusinessCategory).all()

for business_category in business_categories:
    business = session.query(Business).filter(Business.id==business_category.business_id).first()
    business_category.stars = business.stars
    session.add(business_category)

session.commit()
