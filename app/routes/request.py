from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from models.request import Request
import crud.request

from typing import List

app = FastAPI()

@app.get("/requests/", response_model=List[Request])
def read_requests(session: Session = Depends(get_session)):
    try:
        return crud.get_all_requests(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/requests/{request_id}", response_model=Request)
def read_request(request_id: int, session: Session = Depends(get_session)):
    request = crud.get_request_by_id(request_id, session)
    if not request:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    return request

@app.post("/requests/", response_model=Request)
def create_new_request(request: Request, session: Session = Depends(get_session)):
    try:
        new_request = crud.create_request(request, session)
        return new_request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/requests/{request_id}")
def delete_request(request_id: int, session: Session = Depends(get_session)):
    success = crud.delete_request(request_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    return {"detail": "Запрос удален"}

@app.delete("/requests/")
def delete_all_requests(session: Session = Depends(get_session)):
    try:
        count_deleted = crud.delete_all_requests(session)
        return {"deleted_requests": count_deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))