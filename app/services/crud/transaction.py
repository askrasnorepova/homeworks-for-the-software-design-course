from models.transaction import Transaction
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

def get_all_transactions(session: Session) -> List[Transaction]:
    """
    Retrieve all transactions.
    
    Args:
        session: Database session
    
    Returns:
        List[Transaction]: List of all transactions
    """
    try:
        statement = select(Transaction)
        transactions = session.exec(statement).all()
        return transactions
    except Exception as e:
        raise

def get_transaction_by_id(transaction_id: int, session: Session) -> Optional[Transaction]:
    """
    Get transaction by ID.
    
    Args:
        transaction_id: Transactions ID to find
        session: Database session
    
    Returns:
        Optional[Transaction]: Found transaction or None
    """
    try:
        statement = select(Transaction).where(Transaction.id == transaction_id)
        transaction = session.exec(statement).first()
        return transaction
    except Exception as e:
        raise

def create_transaction(transaction: Transaction, session: Session) -> Transaction:
    """
    Create new transaction.
    
    Args:
        transaction: Transactions to create
        session: Database session
    
    Returns:
        Transaction: Created transaction with ID
    """
    try:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
    except Exception as e:
        session.rollback()
        raise
    
def delete_all_transactions(session: Session) -> int:
    """
    Delete all transactions.
    
    Args:
        session: Database session
    
    Returns:
        int: Number of deleted transactions
    """
    try:
        statement = select(Transaction)
        transactions = session.exec(statement).all()
        count = len(transactions)
        
        for transaction in transactions:
            session.delete(transaction)
        
        session.commit()
        return count
    except Exception as e:
        session.rollback()
        raise
    
def delete_transaction(transaction_id: int, session: Session) -> bool:
    """
    Delete transaction by ID.
    
    Args:
        transaction_id: Transactions ID to delete
        session: Database session
    
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        transaction = get_transaction_by_id(transaction_id, session)
        if not transaction:
            return False
            
        session.delete(transaction)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise

