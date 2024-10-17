from databases import Database
import sqlalchemy


DATABASE_URL = "postgresql://user:1234@localhost:5432/library"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)