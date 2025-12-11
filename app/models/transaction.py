from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.request import Request

class TransactionsBase(SQLModel):
    """
    Base transactions model with common fields.
    
    Attributes:
        transaction_size (float): size of transaction
        actual_balance (float): user current balance
    """
    transaction_size: float = Field(..., min = 0.01, max = 999.99)
    actual_balance: float = Field(..., min = 0.00)

class Transaction(TransactionsBase, table=True):
    """
    Transaction model representing transactions in the system.
    
    Attributes:
        id (Optional[int]): Primary key
        user_id (Optional[int]): Foreign key to User
        user (Optional[User]): Relationship to User
        request_id (Optional[int]): Foreign key to Request
        request (Optional[User]): Relationship to Request
        created_at (datetime): Event creation timestamp
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    request_id: Optional[int] = Field(default=None, foreign_key="request.id")
    request: Optional["Request"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def get_actual_balance(self, transaction_size, balance) -> float:
        balance += transaction_size
        return balance

    def __str__(self) -> str:
        result = (f"Id: {self.id}. Creator: {self.user.email}. Transaction size: {self.transaction_size} cr. Balance after transaction: {self.actual_balance} cr. Transaction time: {self.created_at}.")
        return result

class TransactionCreate(TransactionsBase):
     def process_transaction(user, transaction_size, is_replenishment):
        """
        Replenishment or decrease.

        transaction_size: float
        is_replenishment: bool, True if Replenishment, False — decrease
        """

        if is_replenishment:
            if transaction_size < 0:
                raise ValueError("Сумма пополнения не может быть отрицательной")
            actual_balance += transaction_size
        else:
            if transaction_size <= 0:
                raise ValueError("Сумма списания должна быть положительной")
            if actual_balance < transaction_size:
                raise ValueError("Недостаточно средств для списания")
            actual_balance -= transaction_size
        return actual_balance