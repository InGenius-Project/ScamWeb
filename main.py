from fastapi import FastAPI, HTTPException, Form, Request, Response
from typing import List, Dict, Annotated
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import FileResponse, RedirectResponse
from src.service import DataService, DataEntity
from src.constant import HTMLPages
import json

app = FastAPI()
_dataservice = DataService()

BLACK_IP_LIST_FILEPATH = "./src/black_list.json"
BLACK_IP_LIST: set[str] = set()


def refresh_black_list() -> None:
    with open(BLACK_IP_LIST_FILEPATH, "r") as file:
        BLACK_IP_LIST.clear()
        BLACK_IP_LIST.update(set(json.load(file)))


def add_black_list(ip: str):
    BLACK_IP_LIST.add(ip)
    open(BLACK_IP_LIST_FILEPATH, "w").write(str(list(BLACK_IP_LIST)).replace("'", '"'))


def HTMLResponse(path: str):
    return FileResponse(path, media_type="text/html")


@app.exception_handler(HTTPException)
async def not_found_exception_handler(request: Request, exc):
    if exc.status_code == 404:
        if request.client is not None:
            add_black_list(request.client.host)
    elif exc.status_code == 400:
        return Response(status_code=400, content={"message": "Bad Request"})
    return RedirectResponse(url="/err/not_found")


@app.middleware("http")
async def check_blacklist(request: Request, call_next):
    if request.client is None:
        return Response(status_code=400, content="Invalid request.")
    client_ip = request.client.host
    refresh_black_list()
    if client_ip in BLACK_IP_LIST:
        return Response(status_code=403, content="You have been banned.")
    response = await call_next(request)
    return response


@app.get("/err/not_found")
async def not_found():
    return {
        "message": "You have been permanently banned. If any question, please contact the admin."
    }


@app.get("/page/home")
async def home():
    return HTMLResponse(HTMLPages.Path.home)


@app.get("/")
async def root():
    return _dataservice.get_all()


@app.get("/id")
async def get_all_id():
    return _dataservice.get_all_id()


@app.get("/{id}")
async def get_by_id(id: str):
    return _dataservice.get_by_id(id)


@app.post("/")
async def post(data_list: List[Dict]):
    current_ids = _dataservice.get_all_id()
    entity_list = [
        DataEntity(x["id"], x["content"], x["label"])
        for x in data_list
        if x["id"] not in current_ids
    ]
    _dataservice.add_range(entity_list)
    _dataservice.save_change()


@app.get("/article/nocomment")
async def get_nocomment_article():
    article = _dataservice.get_nocomment()
    return article


@app.post("/{id}")
async def change_label(id: str, label: Annotated[int, Form()]):
    if not _dataservice.get_by_id(id):
        raise HTTPException(status_code=400, detail="Id not exist.")

    if label is None:
        raise HTTPException(status_code=400, detail="Label cannot be null.")

    _dataservice.set_label(id, label)
    _dataservice.save_change()
    return RedirectResponse(url="/page/home", status_code=302)
