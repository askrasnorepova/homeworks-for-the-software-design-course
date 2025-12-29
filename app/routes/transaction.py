from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from models.transaction import Transaction
import crud.transaction

from typing import List

app = FastAPI()

@app.get("/transactions/", response_model=List[Transaction])
def read_transactions(session: Session = Depends(get_session)):
    try:
        return crud.get_all_transactions(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = crud.get_transaction_by_id(transaction_id, session)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction

@app.post("/transactions/", response_model=Transaction)
def create_new_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    try:
        new_transaction = crud.create_transaction(transaction, session)
        return new_transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    success = crud.delete_transaction(transaction_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return {"detail": "Транзакция удалена"}

@app.delete("/transactions/")
def delete_all_transactions(session: Session = Depends(get_session)):
    try:
        count_deleted = crud.delete_all_transactions(session)
        return {"deleted_transactions": count_deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))