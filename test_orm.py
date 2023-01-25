"""
https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#user-defined-functions
"""
from Levenshtein import distance
from sqlalchemy import (
    create_engine,
    event,
)
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///:memory:")
@event.listens_for(engine, "connect")
def connect(conn, rec):
    conn.create_function("lsd", 2, distance)

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(bind=engine)

connection = engine.connect()
trans = connection.begin()
try:
    connection.execute('INSERT INTO user(name) VALUES("zztkm")')
    connection.execute('INSERT INTO user(name) VALUES("ジャンボ鶴田")')
    trans.commit()
except:
    trans.rollback()
    raise
trans.close()

print()
print("lsd")
rows = connection.execute('SELECT * FROM user WHERE LSD(name, "tkm") < 3')
for row in rows:
    print(row)

