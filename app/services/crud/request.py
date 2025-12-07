from models.request import Request
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

def get_all_requests(session: Session) -> List[Request]:
    """
    Retrieve all requests.
    
    Args:
        session: Database session
    
    Returns:
        List[Request]: List of all requests
    """
    try:
        statement = select(Request)
        requests = session.exec(statement).all()
        return requests
    except Exception as e:
        raise

def get_request_by_id(request_id: int, session: Session) -> Optional[Request]:
    """
    Get request by ID.
    
    Args:
        request_id: Request ID to find
        session: Database session
    
    Returns:
        Optional[Request]: Found request or None
    """
    try:
        statement = select(Request).where(Request.id == request_id)
        request = session.exec(statement).first()
        return request
    except Exception as e:
        raise

def create_request(request: Request, session: Session) -> Request:
    """
    Create new request.
    
    Args:
        request: Request to create
        session: Database session
    
    Returns:
        Request: Created request with ID
    """
    try:
        session.add(request)
        session.commit()
        session.refresh(request)
        return request
    except Exception as e:
        session.rollback()
        raise
    
def delete_all_requests(session: Session) -> int:
    """
    Delete all requests.
    
    Args:
        session: Database session
    
    Returns:
        int: Number of deleted requests
    """
    try:
        statement = select(Request)
        requests = session.exec(statement).all()
        count = len(requests)
        
        for request in requests:
            session.delete(request)
        
        session.commit()
        return count
    except Exception as e:
        session.rollback()
        raise
    
def delete_request(request_id: int, session: Session) -> bool:
    """
    Delete request by ID.
    
    Args:
        request_id: Request ID to delete
        session: Database session
    
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        request = get_request_by_id(request_id, session)
        if not request:
            return False
            
        session.delete(request)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise

