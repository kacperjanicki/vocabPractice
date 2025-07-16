from sqlalchemy import text,Table,Column,Integer,String,MetaData,create_engine,insert,select
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os

DATABASE_URL = os.getenv("DATABASE_URL")
db = create_engine(DATABASE_URL)
metadata = MetaData()

from schemas.User import User

class DBconnection:

    @staticmethod
    def insertUser(usr: User):
        with Session(db) as session:
            session.add(usr)
            session.commit()

    @staticmethod
    def getUsers() -> list[dict]:
        with Session(db) as session:
            users = session.query(User).all()
            return users


    @staticmethod
    def getUser(name: str) -> dict:
        with Session(db) as session:
            stmt = select(User).where(User.name == name)
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                return {
                    "id": result.id,
                    "name": result.name,
                    "native": result.native,
                    "foreign": result.foreign
                }
            else:
                return {}