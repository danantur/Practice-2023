import re
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from db import news_db, students, teachers


app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def check_if_authed(request: Request, call_next):
    if request.cookies.get("user", None):
        request.state.user = students[int(request.cookies["user"])]
    response = await call_next(request)
    return response


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("site-templates/main.html",
                                      {"request": request,
                                       "news": [news_db[i] | {"id": i} for i in range(3)]})


@app.get("/news")
async def read_news(request: Request):
    shorted_news = list(map(lambda x:
                            {key: " ".join("".join(re.split(r"<[^<>]+>", value)).split()[:20]) + "..." if
                                key == "content" else value for key, value in x.items()}, news_db))
    return templates.TemplateResponse("site-templates/news.html",
                                      {"request": request,
                                       "news": [shorted_news[i] | {"id": i} for i in range(len(shorted_news))]})


@app.get("/new")
async def get_new(request: Request, new_id: int):
    return templates.TemplateResponse("site-templates/new.html",
                                      {"request": request,
                                       "new": news_db[new_id]})


@app.get("/students")
async def read_students(request: Request):
    return templates.TemplateResponse("site-templates/students.html", {"request": request})


@app.get("/adults")
async def read_adults(request: Request):
    return templates.TemplateResponse("site-templates/adults.html", {"request": request})


@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("site-templates/login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    for student_i in range(len(students)):
        student = students[student_i]
        if student["login"] == username and student["pass"] == password:
            resp = JSONResponse("Success", 301, {'Location': '/profile'})
            resp.set_cookie("user", f"{student_i}")
            return resp
    return JSONResponse("Error", 301, {'Location': '/login#error'})


@app.get("/logout")
async def logout(request: Request):
    resp = JSONResponse("Success", 301, {'Location': '/'})
    if request.cookies.get("user", None):
        resp.delete_cookie("user")
    return resp


@app.get("/profile")
async def login_form(request: Request):
    if request.cookies.get("user", None):
        return templates.TemplateResponse("site-templates/profile.html", {"request": request,
                                                                          "teachers": teachers})
    else:
        return JSONResponse("Error", 301, {'Location': '/login'})
