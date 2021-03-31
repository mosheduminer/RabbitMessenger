# RabbitMessenger

> This is a work in progress. Code is not documented or complete.

This is a simple messaging app, featuring direct messaging and group rooms.

All messages are routed through RabbitMQ, to ensure messages are persisted until the appropriate user comes back online. Messages are not stored once they have been delivered.

There are two services, the REST based user registration service (using `FastAPI`), and the websocket based server for all other operations (using `websockets`, and a custom dependency injection and "routing" system).

`Pydantic` is used for validation.

`SQLAlchemy ORM` (with `async` support) is used as an abstraction over `PostgreSQL`.

`Flutter` is used for the frontend. I am developing on the Beta channel, using flutter desktop.
