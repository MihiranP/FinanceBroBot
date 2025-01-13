from pydantic import BaseModel, computed_field, SkipValidation
from sqlalchemy import Engine, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
from visibility.logging import logger
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
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        arbitrary_types_allowed = True

    def connect(self):
        try:
            self.engine = create_engine(self.url)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            logger.info("database connection successful")
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while connecting to the database: {e}")
            raise e

    def close(self):
        self.SessionLocal().close()
        logger.debug("database session closed.")

    def get_db(self):
        if self.SessionLocal is None:
            self.connect()

        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
            logger.debug("Database session closed")

    def create_tables(self):
        try:
            logger.info(f"Attempting to connect to database: {self.name}")
            self.connect()

            if self.engine is None:
                logger.error("Database engine is None - connection failed")
                return

            # Get list of all tables before creation
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()
            logger.info(f"Existing tables before creation: {existing_tables}")

            # Create tables
            self.Base.metadata.create_all(self.engine)

            # Check what tables should have been created
            tables_to_create = [
                table.name for table in self.Base.metadata.sorted_tables
            ]
            logger.info(f"Tables that should be created: {tables_to_create}")

            # Verify tables after creation
            inspector = inspect(self.engine)
            tables_after = inspector.get_table_names()
            logger.info(f"Tables after creation: {tables_after}")

        except SQLAlchemyError as e:
            logger.error(f"An error occurred while creating tables: {e}")
            raise
        finally:
            if self.engine is not None:
                self.engine.dispose()


db = Database()
