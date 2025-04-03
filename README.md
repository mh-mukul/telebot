# FastAPI TeleBot Backend

### Summary

This is a base FastAPI application providing a foundation for building robust and scalable backend services. This application can be used as a starting point for developing various types of backend systems, including REST APIs and microservices. It includes features such as Celery for asynchronous task processing, API key authentication, message sending routes, logging, and custom exceptions.

Key features:

- Database integration with SQLAlchemy
- Database migrations with Alembic
- Command-line interface for managing the application
- Proper logging and error handling
- Redis Celery for processing background tasks
- API endpoint documentation with Swagger UI
- Docker support for easy deployment

Technologies used:

- FastAPI
- SQLAlchemy
- Alembic
- Celery
- Docker

### Project Setup:

- Create python virtual environment & activate it.
- Install the requirements from requirements.txt by running `pip install -r requirements.txt`.
- Create a .env file from `example.env` and fill up the variables.
- Celery Configuration: Configure Celery in `celery_config.py` to connect to a message broker like Redis or RabbitMQ.
- You can select the database of your choice. By default, the application is configured to use SQLite. If you want to use MysQL set `DB_TYPE` to `mysql` and fill up the MYSQL variables.
- Run the application by running `uvicorn app:app --host 0.0.0.0 --port 8001 --reload`. The application server will be running on port 8001 & watch for any changes. Change to your desired port if needed.
- Now you need to run the celery worker for processing background task such as sending telegram messages by running `celery -A celery_config:celery_app worker -l info -c 4`. Here `-c 4` flag determins how many concurrent workers will be running. Increase/decrease based on your need.
- Visit `http://localhost:8001` to verify if the application server has started successfully.
- You can now start building your application on top of this base application.

API Documentation Endpoints(Avaliable only in debug mode):
- `/docs`: Swagger UI documentation for the API endpoints.
- `/redoc`: ReDoc documentation for the API endpoints.

### Database Setup

The application is configured to use SQLite by default. To use a different database, such as MySQL, you will need to update the following environment variables in the `.env` file:

- `DB_TYPE`: Set to `mysql`.
- `DB_HOST`: The hostname or IP address of the database server.
- `DB_PORT`: The port number of the database server.
- `DB_NAME`: The name of the database.
- `DB_USER`: The username for connecting to the database.
- `DB_PASS`: The password for connecting to the database.

After configuring the database connection, you will need to run the database migrations to create the necessary tables. You can do this by running the following command:

```bash
alembic upgrade head
```

### CLI Commands

The following CLI commands are available:

*   `python cli.py generate_key`: Generates a new API key.
*   `python cli.py set_webhook`: Sets the webhook for the Telegram bot.
*   `python cli.py delete_webhook`: Deletes the webhook for the Telegram bot.


### Authentication

The application uses API keys for authentication. The `auth.py` decorator provides a way to protect API endpoints by requiring a valid API key.

### Message Sending

The application can send messages using the `/send-message-group` and `/send-message-private` routes.

-   `/send-message-group`: Sends a message to a Telegram group. It requires a JSON payload with `bot_token`, `group_id`, and `message`. It also accepts optional parameters `thread_id`, `image_url`, and `file_path`.
-   `/send-message-private`: Sends a message to a Telegram user. It requires a JSON payload with `bot_token`, `message`, and either `chat_id` or `mobile`. It also accepts optional parameters `image_url` and `file_path`.

### Deployment

The application can be deployed using Docker. To build the Docker image, run the following command:

```bash
docker build -t telebot-backend .
```

To run the Docker container, run the following command:

```bash
docker-compose up -d
```

Or you can build and run the Docker container in a single command:

```bash
docker-compose up -d --build
```

This will start the application in a detached mode. You can then access the application at `http://localhost:8001`.
