from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import re

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

def validate_username(username):
    """Validate username format."""
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def get_db_session():
    """Create and return a database session."""
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

def delete_user(username):
    """Securely delete a user from the database."""
    if not validate_username(username):
        raise ValueError("Invalid username format")

    session = get_db_session()
    try:
        # Use parameterized query to prevent SQL injection
        query = text("DELETE FROM users WHERE username = :username")
        session.execute(query, {"username": username})
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error: {str(e)}")
    finally:
        session.close()

def main():
    username = input("Enter username to delete: ").strip()
    try:
        if delete_user(username):
            print("User deleted successfully")
        else:
            print("User not found")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except RuntimeError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()