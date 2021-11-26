from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from datetime import datetime
from db_handler import SessionLocal, engine

import re
import crud
import model
import schema

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Users Details",
    description="You can perform CRUD operation by using this API",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/ normalizing_contacts', response_model=List[schema.Contact])
def normalizing_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db=db, skip=skip, limit=limit)
    for contact in contacts:
        contact.gender = gender_normalizer(contact.gender)
        contact.is_married = married_normalizer(contact.is_married)
        contact.birth = birth_check(contact.birth)
        contact.phone = phone_normalizer(contact.phone)
        contact.first_name, contact.last_name = name_normalizer(contact.first_name, contact.last_name)
    return contacts


def birth_check(date):
    try:
        birth = datetime.strptime(date, "%d/%m/%Y")
    except:
        try:
            birth = datetime.strptime(date, "%m/%d/%Y")
        except:
            try:
                birth = datetime.strptime(date, "%B %d, %Y")
            except:
                birth = datetime.strptime(date, "%Y, %B %d")
    birth = birth.strftime("%d/%m/%Y")
    return birth


def phone_normalizer(phone):
    pattern = '^(\+98)\d{10}$'
    regexp = re.compile(pattern)
    if regexp.match(phone):
        return phone
    else:
        phone = phone[1:]
        phone = '+98'+phone
        return phone


def name_normalizer(first_name, last_name):
    first = []
    last = []
    if (last_name is None or last_name == "") and (first_name is not None):
        name_list = first_name.split()
        if len(name_list) > 2:
            first = name_list[:2]
            last = name_list[2:]
        elif len(name_list) == 2:
            first = name_list[:1]
            last = name_list[1:]
    elif (first_name is None) and (last_name is not None):
        last_list = last_name.split()
        if len(last_list) > 2:
            first = last_list[:2]
            last = last_list[2:]
        elif len(last_list) == 2:
            first = last_list[:1]
            last = last_list[1:]
    else:
        last_list = last_name.split()
        name_list = first_name.split()
        if last_list == name_list:
            first = name_list[:1]
            last = last_list[1:]
        elif name_list[0] == 'Mr.' or name_list[0] == 'Mrs.':
            first = last_list[1:]
            last = last_list[:1]
        else:
            first = name_list
            last = last_list
    first_name = " ".join(str(x) for x in first)
    last_name = " ".join(str(x) for x in last)
    return first_name, last_name


def gender_normalizer(gender):
    if gender == "Male":
        gender = 'M'
    if gender == "Female":
        gender = 'F'
    return gender


def married_normalizer(is_married):
    married = ['yes', 'married', 'true', 'Yes', 'True']
    if is_married in married:
        is_married = True
    else:
        is_married = False
    return is_married
