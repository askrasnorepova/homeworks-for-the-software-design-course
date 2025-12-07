from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from pydub import AudioSegment
import magic
import math

if TYPE_CHECKING:
    from models.user import User
    from models.transaction import Transaction

class RequestsBase(SQLModel):
    """
    Base requests model with common fields.
    
    Attributes:
        audio(str): path to file with audio recording
        duration(float): audio recording duration (s)
        cost(float): cost of request
        transript(str): result of transcription
    """
    audio: str = Field(...)
    duration: float = Field(..., min = 5, max = 600)
    cost: float = Field(...)
    transcript: str = Field(..., max_length = 30000)

    def _validate_request(self) -> None:
        """Validate uploaded file"""
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(audio)
        if 'audio' not in file_type:
            raise ValueError("Invalid request format. Please upload audio")
        
    def get_duration(self, audio) -> None:
        """Determines duration of uploaded audio recording"""
        audio_file = AudioSegment.from_file(audio)
        dur_audio = audio_file.duration_seconds
        return dur_audio

    def get_price(self) -> None:
        """Determines request cost"""
        duration_audio = self.get_duration()
        price = duration_audio * 0,25 # 0,25 cr. is cost of 1 second audio 
        return price

class Request(RequestsBase, table=True):
    """
    Request model representing requests in the system.
    
    Attributes:
        id (Optional[int]): Primary key
        user_id (Optional[int]): Foreign key to User
        user (Optional[User]): Relationship to User
        transaction_id (Optional[int]): Foreign key to Transaction
        transaction (Optional[Transaction]): Relationship to Transaction
        created_at (datetime): Event creation timestamp
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(
        back_populates="requests",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id")
    transaction: Optional["Transaction"] = Relationship(
        back_populates="requests",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    

    def __str__(self) -> str:
        result = (f"Id: {self.id}. Creator: {self.user.email}. Audio: {self.title}. Audio duration: {self.duration} s. Request cost: {self.cost} cr. Request time: {self.created_at}.")
        return result  

class RequestCreate(RequestsBase):
    """Schema for creating new events"""
    pass