import time
from datetime import datetime
from typing import Optional
from string import ascii_letters, digits
from random import choice

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

CHARACTERS = ascii_letters + digits
SIZE = 7


class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num_follows: int = 0
    long_url: str
    short_url: str
    code: str

    @staticmethod
    def create_code(chars=CHARACTERS):
        return "".join([choice(chars) for _ in range(SIZE)])
