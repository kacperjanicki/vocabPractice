import httpx
from fastapi.responses import JSONResponse
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String,LargeBinary
import json

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # fields below will be fetched from openlibrary.org API
    author_name: Mapped[str] = mapped_column(String(100), nullable=True)
    cover: Mapped[bytes] = mapped_column("cover",LargeBinary, nullable=True)

    def __init__(self, title: str, author_name: str = None, cover: bytes = None):
        self.title = title
        self.cover = cover
        self.author_name = author_name
    
    def __repr__(self) -> str:
        return f"Book_id: {self.book_id}, title:{self.title}, author_name:{self.author_name}, coverBytes: {self.cover}"
    
    def setMetadata(self, metadata: list[dict]) -> None:
        """
            Here, we override the data that user entered e.g 'title'
            because he might have enterered 'no rules rules' (all lowercase),
            we found the record in openlibrary api and its in camel case
            'No Rules Rules' looks more elegant, thats why we override it
        """
        # for now, only author_name

        # figure out, how to let user pick from different covers

        # print(json.dumps(metadata,indent=2))
        self.author_name = metadata[0]["author_name"]
        self.title = metadata[0]["title"]
        self.cover = metadata[0]["cover_i"]

    async def fetchMetadata(self) -> JSONResponse:
        url = f"https://openlibrary.org/search.json?q={self.title}&fields=key,title,cover_i,author_name,editions,editions.key,editions.title,editions.language"
        async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.get(
                    url=url
                )
                data = response.json()
                needed=[
                    {
                        "author_name":doc.get("author_name",[]),
                        "title":doc.get("title",[]),
                        "cover_i":doc.get("cover_i",[])
                    }
                    for doc in data.get('docs',[])
                    if isinstance(doc.get("cover_i"), int) # dont show book entries that dont have a cover image
                ]
                self.setMetadata(needed)

                return JSONResponse(needed)


