from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(length=30))
    lastname = Column(String(length=70))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Contact: %s>' % self.name


def create_example_contacts():
    sballmer = Contact('Steve Ballmer')
    sjobs = Contact('Steve Jobs')
    mzuckerberg = Contact('Mark Zuckerberg')

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(
        'mysql://alexander:@localhost/alembic_content_migration_example'
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(sballmer)
    session.add(sjobs)
    session.add(mzuckerberg)
    session.commit()
