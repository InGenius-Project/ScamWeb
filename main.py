from fastapi import FastAPI, HTTPException, Form
from typing import List, Dict, Annotated
from fastapi.responses import FileResponse, RedirectResponse
from src.service import DataService, DataEntity
from src.constant import HTMLPages

app = FastAPI()
_dataservice = DataService()


def HTMLResponse(path: str):
    return FileResponse(path, media_type="text/html")


@app.exception_handler(404)
async def not_found_exception_handler(_, __):
    return RedirectResponse(url="/err/not_found")


@app.get("/err/not_found")
async def not_found():
    return {"message": "Page not found. To Hacker, go tryhackme.com, not here."}


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
