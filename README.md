# Contact Management API

This is a FastAPI-based Contact Management System that allows users to add and manage contact information while enforcing precedence rules for phone numbers and emails.

## Features

- Add contacts with phone numbers and emails.
- Maintain one primary phone number and one primary email at a time.
- Automatically update contact precedence when a new primary is set.
- Retrieve primary and secondary contacts in a structured JSON response.
- Uses PostgreSQL with SQLAlchemy for data storage.

## Tech Stack

- **FastAPI** - Web framework for building APIs
- **SQLAlchemy** - ORM for database interactions
- **PostgreSQL** - Database for storing contact information
- **Uvicorn** - ASGI server for running FastAPI

## Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/AmoghAgrawal1249/Identity.git
   cd contact-management-api
   ```

2. **Set up a virtual environment**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database**  
   - Update `DATABASE_URL` in `model.py` to point to your PostgreSQL database.
   - Create tables using SQLAlchemy:
     ```sh
     python model.py
     ```

5. **Run the FastAPI server**  
   ```sh
   uvicorn Endpoint:app --reload
   ```

6. **Test the API**  
   Open your browser and go to:  
   ```
   http://127.0.0.1:8000/docs
   ```
   This will open the interactive API documentation.

## API Endpoints

### Add or Update Contact  
**Endpoint:**  
```http
POST /identity/
```
**Query Parameters:**
- `phone` (string) - Phone number of the contact
- `email` (string) - Email of the contact
- `precedence_phone` (boolean) - Whether the phone number should be primary
- `precedence_email` (boolean) - Whether the email should be primary

**Example Request:**  
```sh
curl -X 'POST' 'http://127.0.0.1:8000/identity/?phone=1234567890&email=example@email.com&precedence_phone=true&precedence_email=false' -H 'accept: application/json' -d ''
```

**Example Response:**  
```json
{
  "Error": false,
  "Contactid": 1,
  "Created": "2025-03-24T16:46:34.860471",
  "Updated": "2025-03-24T18:17:59.587703",
  "Primary Contact": "1234567891",
  "Primary Email": "example@email.com",
  "Secondary Contacts": [
    "1111111111",
    "9876543210"
  ],
  "Secondary Emails": [
    "alt@email.com"
  ]
}
```

## Project Structure

```
contact-management-api/
│── Endpoint.py       # FastAPI implementation for contact management
│── model.py          # SQLAlchemy models and database setup
│── requirements.txt  # Required dependencies
│── README.md         # Project documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch:  
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Your commit message"
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Open a pull request.


