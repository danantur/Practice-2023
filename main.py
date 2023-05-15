import re

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


from news import news_db

app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("site-templates/main.html",
                                      {"request": request,
                                       "news": [news_db[i] | {"id": i} for i in range(3)]})


@app.get("/news")
def read_news(request: Request):
    shorted_news = list(map(lambda x: {key: " ".join("".join(re.split(r"<[^<>]+>", value)).split()[:20]) + "..." if key == "content" else value for key, value in x.items()}, news_db))
    return templates.TemplateResponse("site-templates/news.html",
                                      {"request": request,
                                       "news": [shorted_news[i] | {"id": i} for i in range(len(shorted_news))]})


@app.get("/new")
def get_new(request: Request, new_id: int):
    return templates.TemplateResponse("site-templates/new.html",
                                      {"request": request,
                                       "new": news_db[new_id]})


@app.get("/students")
def read_students(request: Request):
    return templates.TemplateResponse("site-templates/students.html", {"request": request})


@app.get("/adults")
def read_adults(request: Request):
    return templates.TemplateResponse("site-templates/adults.html", {"request": request})
