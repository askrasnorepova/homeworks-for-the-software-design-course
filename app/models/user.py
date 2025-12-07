from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from passlib.hash import bcrypt
import re

if TYPE_CHECKING:
    from models.requests import Request
    from models.transactions import Transaction

class User(SQLModel, table=True): 
    """
    User model representing application users.
    
    Attributes:
        id (int): Primary key
        email (str): User's email address
        password (str): Hashed password
        created_at (datetime): Account creation timestamp
        requests (List[Request]): List of user's requests
        transactions (List[Transaction]): List of user's transaction
        actual_balance (float): User's balance
        is_admin (bool): user's administrator rights
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        ...,  # Required field
        unique=True,
        index=True,
        min_length=5,
        max_length=255
    )
    password: str = Field(..., min_length=8) 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    transactions: List["Transaction"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )
    requests: List["Request"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )

    actual_balance: float = Field(default = 0)

    is_admin: bool = Field (default = False)
    
    def __str__(self) -> str:
        return f"Id: {self.id}. Email: {self.email}"

    def validate_email(self) -> bool:
        """
        Validate email format.
        
        Returns:
            bool: True if email is valid
        
        Raises:
            ValueError: If email format is invalid
        """
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(self.email):
            raise ValueError("Invalid email format")
        return True
    
    def validate_password(self) -> bool:
        """
        Validate password format.
        
        Returns:
            bool: True if password is valid
        
        Raises:
            ValueError: If password is too easy
        """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if not pattern.match(self.password):
            raise ValueError("Password is too easy")
        return True
    
    def hash_password(self, password):
        return bcrypt.hash(password)
    
    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
    @property
    def requests_count(self) -> int:
        """Number of requests associated with user"""
        return len(self.requests)
    
    @property
    def transactions_count(self) -> int:
        """Number of transactions associated with user"""
        return len(self.transactions) 

    class Config:
        """Model configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True

    def change_user_balance(id, user_balance, is_admin):
        """Change user balance"""
        if is_admin == True:
            change = input(int('Введите сумму, на которую необходимо изменить баланс. Если Вы хотите уменьшить баланс, введите сумму со знаком "-"'))
            user_balance[id] += change
