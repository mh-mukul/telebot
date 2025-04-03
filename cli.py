import asyncio
import secrets
import argparse
from telegram import Bot
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


async def set_webhook():
    """Sets the webhook for the Telegram bot."""
    token = input("Enter your bot token: ")
    url = input("Enter your webhook URL: ")
    if not token or not url:
        print("Both token and URL are required.")
        return
    bot = Bot(token=token)
    try:
        await bot.delete_webhook()  # Delete any existing webhook
        await bot.set_webhook(url)
        print(f"Webhook set to: {url}")
    except Exception as e:
        print(f"Failed to set webhook: {e}")


async def delete_webhook():
    """Deletes the webhook for the Telegram bot."""
    token = input("Enter your bot token: ")
    if not token:
        print("Token is required.")
        return
    bot = Bot(token=token)
    try:
        await bot.delete_webhook()
        print("Webhook deleted.")
    except Exception as e:
        print(f"Failed to delete webhook: {e}")


def main():
    db = next(get_db())
    parser = argparse.ArgumentParser(description="Management Commands")
    parser.add_argument("command", help="Command to run",
                        choices=["generate_key", "set_webhook", "delete_webhook"])

    args = parser.parse_args()

    if args.command == "generate_key":
        generate_key(db)
    elif args.command == "set_webhook":
        asyncio.run(set_webhook())
    elif args.command == "delete_webhook":
        asyncio.run(delete_webhook())


if __name__ == "__main__":
    main()
