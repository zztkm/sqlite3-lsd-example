"""
https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#user-defined-functions
"""
from Levenshtein import distance
from sqlalchemy import (
    create_engine,
    event,
)
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("sqlite:///:memory:")
Base = declarative_base()

@event.listens_for(engine, "connect")
def connect(conn, rec):
    conn.create_function("lsd", 2, distance)


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

s = Session()

# データ作成
user1 = User(name="zztkm")
user2 = User(name="ジャンボ鶴田")
s.add_all([user1, user2])
s.commit()

rows = s.query(User).all()
print("all user")
for row in rows:
    print(row.name)


# レーベシュタイン距離が 3 未満のレコードを取得する
print()
print("lsd")
rows = s.execute('SELECT * FROM user WHERE LSD(name, "tkm") < 3')
for row in rows:
    print(row)
