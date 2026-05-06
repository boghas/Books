from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: str

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: str) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    rating: int = Field(gt=0, lt=6)
    published_date: str = Field(
        min_length=8, max_length=8, description="The date it was published. It must be exactly 8 characters long."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book title. Must be at least three characters long.",
                "author": "A new book author. Must be at least three characters long.",
                "description": "A new book description. Must be between three and fifty characters long.",
                "rating": "A new book rating. Must be an integer between (0, 6).",
                "published_date": "The published date. Must be exactly 8 characters long. Example: 01022026.",
            }
        }
    }


BOOKS: list[Book] = [
    Book(1, 'Computer Science Pro', 'Bogdan', 'A good book', 5, "01022026"),
    Book(2, 'Be Fast with FastAPI', 'Bogdan', 'A great book', 5, "10022026"),
    Book(3, 'Master Endpoints', 'Bogdan', 'An awesome book', 5, "01022025"),
    Book(4, 'HP1', 'Author One', 'Book description', 2, "01042026"),
    Book(5, 'HP2', 'Author Two', 'Book description', 3, "10042026"),
    Book(6, 'HP3', 'Author Three', 'Book description', 1, "01022026"),
]


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.get('/books')
async def get_all_books():
    return BOOKS


@app.get('/book/{book_id}')
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="The book does not exist")
        

@app.get('/book/')
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]

    return books_to_return

@app.get('/books/{published_date}')
async def get_book_by_published_date(published_date: str = Path(min_length=8, max_length=8)):
    books_to_return = [book for book in BOOKS if book.published_date == published_date]

    return books_to_return


@app.post('/create_book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put('/books/update_book')
async def update_book(book_request: BookRequest):
    book_found = False
    for i in range(0, len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            book_found = True
            new_book = Book(**book_request.model_dump())
            BOOKS[i] = new_book
            break
    
    if not book_found:
        raise HTTPException(status_code=404, detail="Book does not exist!")
    

@app.delete('/books/{book_id}')
async def delete_book(book_id: int = Path(gt=0)):
    book_found = False
    for i in range(0, len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_found = False
            break

    if not book_found:
        raise HTTPException(status_code=404, detail="Book not found")

