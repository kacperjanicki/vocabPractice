import httpx
from fastapi.responses import JSONResponse
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    native: Mapped[str] = mapped_column("native_iso_code",String(3), nullable=False)
    foreign: Mapped[str] = mapped_column("foreign_iso_code",String(3), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100),nullable=False)

    def __repr__(self):
        return f"Name: {self.name}, Native: {self.native}, Foreign: {self.foreign}"

    # async def getMetadata(self) -> JSONResponse:
    #     url = f"https://openlibrary.org/search.json?q={self.title}&fields=key,title,cover_i,author_name,editions,editions.key,editions.title,editions.language"
    #     async with httpx.AsyncClient(timeout=120.0) as client:
    #             response = await client.get(
    #                 url=url
    #             )
    #             data = response.json()
    #             needed=[
    #                 {
    #                     "author_name":doc.get("author_name",[]),
    #                     "title":doc.get("title",[]),
    #                     "cover_i":doc.get("cover_i",[])
    #                 }
    #                 for doc in data.get('docs',[])
    #                 if isinstance(doc.get("cover_i"), int) # dont show book entries that dont have a cover image
    #             ]

    #             self.setMetadata(needed)
    #             return JSONResponse(needed)

