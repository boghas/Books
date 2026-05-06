from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    rating: int = Field(gt=0, lt=6)


BOOKS: list[Book] = [
    Book(1, 'Computer Science Pro', 'Bogdan', 'A good book', 5),
    Book(2, 'Be Fast with FastAPI', 'Bogdan', 'A great book', 5),
    Book(3, 'Master Endpoints', 'Bogdan', 'A awesome book', 5),
    Book(4, 'HP1', 'Author One', 'Book description', 2),
    Book(5, 'HP2', 'Author Two', 'Book description', 3),
    Book(6, 'HP3', 'Author Three', 'Book description', 1)
]


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.get('/books')
async def get_all_books():
    return BOOKS


@app.post('/create_book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))