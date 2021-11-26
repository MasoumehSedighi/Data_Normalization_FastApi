from sqlalchemy.orm import Session
import model


def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> object:
    return db.query(model.Contacts).offset(skip).limit(limit).all()
