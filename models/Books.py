from sqlalchemy import Table, Column, Integer, String
from database import metadata

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String(200)),
    Column("author", String(100)),
    Column("description", String),
    Column("link", String(50))
)