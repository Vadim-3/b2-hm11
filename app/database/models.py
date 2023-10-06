from sqlalchemy import Column, Integer, String, Date
from connect import Base, engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    birthday_date = Column(Date)
    emails = Column(String, nullable=False, index=True)
    phone_numbers = Column(String, nullable=False, index=True)
    other_description = Column(String, nullable=True, default=None)


Base.metadata.create_all(bind=engine)
