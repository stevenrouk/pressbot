import contextlib
from sqlalchemy import create_engine, MetaData

from config import SQLITE_DATABASE_URI

engine = create_engine(SQLITE_DATABASE_URI)
meta = MetaData(bind=engine)
meta.reflect()

for table in reversed(meta.sorted_tables):
    engine.execute(table.delete())
