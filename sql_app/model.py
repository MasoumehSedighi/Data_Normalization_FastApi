from sqlalchemy import Boolean, Column, String
from db_handler import Base


class Contacts(Base):

    __tablename__ = "contacts"

    first_name = Column(String(255), index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    birth = Column(String,  primary_key=True, autoincrement=True, index=True, nullable=True)
    gender = Column(String, index=True, nullable=True)
    is_married = Column(Boolean, nullable=False)
    phone = Column(String(255), index=True, nullable=True)

