from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.database import get_session
from models.request import Request
from typing import List

request_router = APIRouter()
requests = []

@request_router.get("/", response_model=List[Request]) 
async def retrieve_all_requests() -> List[Request]:
    return requests

@request_router.get("/{id}", response_model=Request) 
async def retrieve_request(id: int) -> Request:
    for request in requests: 
        if request.id == id:
            return request 
    raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="Request with supplied ID does not exist")

@request_router.post("/new")
async def create_request(body: Request = Body(...)) -> dict: 
    requests.append(body)
    return {"message": "Request created successfully"}

@request_router.delete("/{id}")
async def delete_event(id: int) -> dict: 
    for request in requests:
        if request.id == id: 
            requests.remove(request)
            return {"message": "Request deleted successfully"}
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="Request with supplied ID does not exist")

@request_router.delete("/")
async def delete_all_requests() -> dict: 
    requests.clear()
    return {"message": "Requests deleted successfully"}