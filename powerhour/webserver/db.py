from decimal import Decimal

import databases
import sqlalchemy


DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

generate_power_hour_jobs = sqlalchemy.Table(
    "generate_power_hour_jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, nullable=False, primary_key=True),
    sqlalchemy.Column("playlist_url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("youtube_api_key", sqlalchemy.String, nullable=True, default=None),
    sqlalchemy.Column("videos_processed", sqlalchemy.Integer, nullable=False, default=0),
    sqlalchemy.Column("completion_percentage", sqlalchemy.DECIMAL, nullable=False, default=Decimal(0)),
    sqlalchemy.Column("output_file", sqlalchemy.String, nullable=True, default=None),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
