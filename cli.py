import secrets
import argparse
from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db

from models import ApiKey


def generate_key(db: Session = Depends(get_db)):
    """Generates a new API key."""
    new_key = secrets.token_urlsafe(32)  # Generate a random key
    api_key = ApiKey(key=new_key)

    db.add(api_key)
    db.commit()

    print(f"New API key generated: {new_key}")


def main():
    db = next(get_db())
    parser = argparse.ArgumentParser(description="Management Commands")
    parser.add_argument("command", help="Command to run",
                        choices=["generate_key", "create_department", "create_superuser", "create_module", "create_permission"])

    args = parser.parse_args()

    if args.command == "generate_key":
        generate_key(db)


if __name__ == "__main__":
    main()
