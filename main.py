from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("site-templates/main.html", {"request": request})


@app.get("/news")
def read_root(request: Request):
    return templates.TemplateResponse("site-templates/news.html", {"request": request})


@app.get("/students")
def read_root(request: Request):
    return templates.TemplateResponse("site-templates/students.html", {"request": request})


@app.get("/adults")
def read_root(request: Request):
    return templates.TemplateResponse("site-templates/adults.html", {"request": request})
