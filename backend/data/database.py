from pydantic import BaseModel, computed_field, SkipValidation
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
from config.settings import app_settings


class Database(BaseModel):
    user: str = app_settings.postgres_db_user
    password: str = app_settings.postgres_db_password
    host: str = app_settings.postgres_db_host
    port: str = app_settings.postgres_db_port
    name: str = app_settings.postgres_db_name
    engine: SkipValidation[Engine] | None = None
    SessionLocal: SkipValidation[sessionmaker] | None = None
    Base: Any = declarative_base()

    @computed_field
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def connect(self) -> None:
        try:
            self.engine = create_engine(self.url)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
        except SQLAlchemyError as e:
            # TODO: Add logging bruv
            raise e

    def close(self):
        self.SessionLocal().close()
        # app_logger.debug("database session closed.")

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        try:
            self.connect()
            self.Base.metadata.create_all(self.engine)
        # TODO: set up logging
        #     app_logger.debug("Tables created successfully")
        # except SQLAlchemyError as e:
        #     app_logger.error(f"An error occurred while creating tables: {e}")
        finally:
            self.engine.dispose()


db = Database()
