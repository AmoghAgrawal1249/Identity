from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from model import Contact, SessionLocal
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identity/")
def add_contact(phone: str, email: str, precedence_phone: bool, precedence_email: bool, db: Session = Depends(get_db)):
    if not phone and not email:
        raise HTTPException(status_code=400, detail="At least one of phone or email must be provided.")

    existing_contact = db.query(Contact).filter(
        Contact.phone == phone, Contact.email == email
    ).first()

    # Ensure only one phone and one email are primary
    if precedence_phone:
        db.query(Contact).filter(Contact.phone != phone, Contact.linkprecedence_phone == True).update({"linkprecedence_phone": False}, synchronize_session=False)
        db.query(Contact).filter(Contact.phone == phone).update({"linkprecedence_phone": True}, synchronize_session=False)
    else:
        db.query(Contact).filter(Contact.phone == phone).update({"linkprecedence_phone": False}, synchronize_session=False)

    if precedence_email:
        db.query(Contact).filter(Contact.email != email, Contact.linkprecedence_email == True).update({"linkprecedence_email": False}, synchronize_session=False)
        db.query(Contact).filter(Contact.email == email).update({"linkprecedence_email": True}, synchronize_session=False)
    else:
        db.query(Contact).filter(Contact.email == email).update({"linkprecedence_email": False}, synchronize_session=False)

    if existing_contact:
        # Update existing contact
        existing_contact.linkprecedence_phone = precedence_phone
        existing_contact.linkprecedence_email = precedence_email
        existing_contact.modified_at = datetime.utcnow()
    else:
        # Create new contact
        new_contact = Contact(
            phone=phone,
            email=email,
            linkprecedence_phone=precedence_phone,
            linkprecedence_email=precedence_email,
            created_at=datetime.utcnow(),
            modified_at=datetime.utcnow()
        )
        db.add(new_contact)
        db.flush()
        db.commit()
        
    db.commit()

    # Fetch primary phone
    primary_phone = db.query(Contact).filter(Contact.linkprecedence_phone == True).first()
    primary_email = db.query(Contact).filter(Contact.linkprecedence_email == True).first()
    
    # Fetch secondary contacts
    secondary_contacts = db.query(Contact.phone).filter(
        Contact.linkprecedence_phone == False
    ).all()
    secondary_emails = db.query(Contact.email).filter(
        Contact.linkprecedence_email == False
    ).all()

    new_contact = db.query(Contact).filter(
        Contact.phone == phone, Contact.email == email
    ).first()

    return {
        "Error": False,
        "Contactid": existing_contact.id if existing_contact else new_contact.id,
        "Created": existing_contact.created_at if existing_contact else new_contact.created_at,
        "Updated": existing_contact.modified_at if existing_contact else new_contact.modified_at,
        "Primary Contact": primary_phone.phone if primary_phone else None,
        "Primary Email": primary_email.email if primary_email else None,
        "Secondary Contacts": list(set(c[0] for c in secondary_contacts if c[0] is not None)),
        "Secondary Emails": list(set(c[0] for c in secondary_emails if c[0] is not None))
    }


from model import SessionLocal

db = SessionLocal()
print("Connected to DB:", db.bind.url)
db.close()
