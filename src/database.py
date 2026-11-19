import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:sabiha%4012345@localhost:3306/ticket_db",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def migrate_ticket_columns():
    if engine.dialect.name != "mysql":
        return

    column_specs = {
        "email": ("VARCHAR(254)", 254),
        "message": ("TEXT", None),
        "urgency": ("VARCHAR(10)", 10),
        "subject": ("VARCHAR(255)", 255),
    }

    with engine.begin() as connection:
        columns = {
            column["name"]: column["type"]
            for column in inspect(connection).get_columns("tickets")
        }
        for name, (sql_type, expected_length) in column_specs.items():
            if getattr(columns[name], "length", None) != expected_length:
                connection.execute(
                    text(
                        f"ALTER TABLE tickets MODIFY COLUMN {name} "
                        f"{sql_type} NULL"
                    )
                )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()