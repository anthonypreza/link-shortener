import os
import posixpath
from typing import Optional

import validators
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models.link import Link

dir_ = os.path.dirname(__file__)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory=f"{dir_}/static"), name="static")

templates = Jinja2Templates(directory=f"{dir_}/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/shorten")
async def shorten_link(request: Request):
    form_data = await request.form()
    url = form_data["url"] if "url" in form_data else ""

    if not validators.url(url):
        return templates.TemplateResponse(
            "home.html", {"request": request, "errors": "Please provide a valid URL."}
        )

    def get_unique_code(session: Session):
        code = Link.create_code()
        statement = select(Link).where(Link.code == code)
        results = session.exec(statement)

        if results.first() is not None:
            return get_unique_code(session)

        return code

    with Session(engine) as session:
        code = get_unique_code(session)
        short_url = posixpath.join(request.url_for("home"), code)
        link = Link(long_url=url, code=code, short_url=short_url)

        session.add(link)
        session.commit()
        session.refresh(link)

    return templates.TemplateResponse(
        "home.html", {"request": request, "long_url": url, "short_url": short_url}
    )


@app.get("/{code}")
async def redirect(code: str):
    with Session(engine) as session:
        statement = select(Link).where(Link.code == code)
        results = session.exec(statement)
        link = results.first()

        if link is not None:
            link.num_follows += 1
            session.add(link)
            session.commit()
            session.refresh(link)
            return RedirectResponse(link.long_url)

    raise HTTPException(404, "This link is broken 😔")
