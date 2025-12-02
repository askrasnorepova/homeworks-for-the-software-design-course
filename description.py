from sqlmodel import SQLModel, Field, Relationship, Session, select
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydub import AudioSegment
import re
import magic
import math


class User(SQLModel, table=True):
    """
    Класс для представления пользователя в системе.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Пароль пользователя
        actual_balance(float): Текущий баланс
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        unique=True,
        index=True,
        min_length=5,
        max_length=255
    )
    password: str = Field(min_length=8) 
    actual_balance: float = Field()

    def __str__(self) -> str:
        return f"Id: {self.id}. Email: {self.email}"

    def __post_init__(self) -> bool:
        self._validate_email()
        self._validate_password()

    def _validate_email(self) -> bool:
        """Проверяет корректность email."""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self) -> None:
        """Проверяет минимальную длину пароля."""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
    
    def get_all_users(session: Session) -> List[User]:
        try:
            statement = select(User).options(
                selectinload(User.events).selectinload(Event.creator)
            )
            users = session.exec(statement).all()
            return users
        except Exception as e:
            raise

    def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
        try:
            statement = select(User).where(User.id == user_id).options(
                selectinload(User.request)
            )
            user = session.exec(statement).first()
            return user
        except Exception as e:
            raise

    def create_user(user: User, session: Session) -> User:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise

    def delete_user(user_id: int, session: Session) -> bool:
        try:
            user = get_user_by_id(user_id, session)
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise


class Request(SQLModel, table=True):
    """
    Класс запросов пользователя на расшифровку аудиозаписи

    Attributes:
        request_id(int): id запроса, primary key
        audio(str): путь к файлу с аудиозаписью
        duration(float): длительность аудиозаписи
        cost(float): стоимость запроса
        user_id(int): id пользователя, foreign key
        transaction_id(int): id транзакции, foreign key
    """

    request_id: int = Field(default=None, primary_key=True)
    audio: str = Field()
    duration: float = Field()
    cost: float = Field()
    request_history: List['Request'] = Field(default_factory=list)
    user_id: int = Field(default=None, foreign_key=True)
    transaction_id: int = Field(default=None, foreign_key=True)

    user = Relationship('User', back_populates='Request')
    transaction = Relationship('Transaction', back_populates='Request')

    def __post_init__(self) -> None:
        self._validate_request()

    def _validate_request(self) -> None:
        """Проверяет корректность запроса"""
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(audio)
        if 'audio' not in file_type:
            raise ValueError("Invalid request format. Please upload audio")
        
    def get_duration(self, audio) -> None:
        """Определяет длительность загруженной аудиозаписи"""
        audio_file = AudioSegment.from_file(audio)
        dur_audio = audio_file.duration_seconds
        return dur_audio

    def get_price(self, cost) -> None:
        """Определяет стоимость запроса"""
        duration_audio = self.get_duration()
        price = math.ceil(duration_audio / cost)
        return price
    
    def get_all_requests(session: Session) -> List[Request]:
        try:
            statement = select(Request).options(
                selectinload(User.requests).selectinload(Request.user)
            )
            requests = session.exec(statement).all()
            return requests
        except Exception as e:
            raise

    def get_request_by_id(request_id: int, session: Session) -> Optional[Request]:
        try:
            statement = select(Request).where(Request.id == request_id).options(
                selectinload(Request.User)
            )
            request = session.exec(statement).first()
            return request
        except Exception as e:
            raise

    def create_request(request: Request, session: Session) -> Request:
        try:
            session.add(request)
            session.commit()
            session.refresh(request)
            return request
        except Exception as e:
            session.rollback()
            raise


class Request_History(Request, table = True):
    """
    Класс для представления истории запросов
    
    Attributes:
        request_id(Optional[int]): Primary key
        user_id (Optional[int]): Foreign key to User
        transaction_id(Optional[int]): Foreign key to Transaction
        created_at (datetime): Event creation timestamp
    """
    request_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.transaction_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __str__(self) -> str:
        result = (f"Request id: {self.request_id}. Audio: {self.audio}. Creator: {self.user.email}. Created at: {self.created_at}. Cost of request: {self.transaction.decrease}.")
        return result
    
    def __init__ (self) -> None:
        self.request_history = []

    def add_to_request_history(self, request: 'Request') -> None:
        """Добавляет запрос в список запросов пользователя."""
        self.request_history.append(request)
    
    def get_all_requests(self):
        """Возвращает список всех запросов пользователя"""
        return self.request_history

class RequestCreate(Request):
    """Schema for creating new requests"""
    pass

class Model:
    """
    Класс для вызова модели
    
    Attributes:
        model (str): путь к размещению модели
    """
    model: str

    def use_model(self) -> None:
        return model(audio)


class Transaction (SQLModel):
    """ Класс для представления финансовых операций пользователя

    Attributtes:
        transaction_id(int): id операции, primary key
        actual_balance(float): Текущий баланс
        replenishment (float): Сумма пополнения
        decrease (float): Сумма списания за запрос
        user_id(int): id пользователя, foreign key
    """

    transaction_id: int = Field(default=None, primary_key=True)
    replenishment: float = Field(default=None)
    decrease: float = Field(default=None)
    transaction_history: (list['Transaction']) = Field(default_factory=list)
    user_id: int = Field(default=None, foreign_key=True)
    request_id: int = Field(default=None, foreign_key=True)

    user = Relationship('User', back_populates='Transaction')
    request = Relationship('Request', back_populates='Request')

    def replenish_balance(self, replenishment, transaction: 'Transaction') -> None:
        """Пополняет баланс пользователя"""
        actual_balance += replenishment
        transaction = replenishment
        return f"Ваш баланс пополнен на {replenishment} кр. На Вашем счете: {actual_balance} кр."
    
    def decrease_balance(self) -> None:
        """Списание средств за новый запрос"""
        request = Request
        decrease = request.get_price()
        actual_balance -= decrease
        return f"С Вашего счета списано {decrease} кр. На Вашем счете: {actual_balance} кр."
    
    def get_all_transactions(session: Session) -> List[Transaction]:
        try:
            statement = select(Transaction).options(
                selectinload(User.Transaction).selectinload(Transaction.user)
            )
            transactions = session.exec(statement).all()
            return transactions
        except Exception as e:
            raise

    def get_transaction_by_id(transaction_id: int, session: Session) -> Optional[Transaction]:
        try:
            statement = select(Transaction).where(Transaction.transaction_id == transaction_id).options(
                selectinload(Transaction.User)
            )
            transaction = session.exec(statement).first()
            return transaction
        except Exception as e:
            raise

    def create_transaction(transaction: Transaction, session: Session) -> Transaction:
        try:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return transaction
        except Exception as e:
            session.rollback()
            raise
    
class Transaction_History(Transaction, table = True):
    """
    Класс для представления истории транзакций
    
    Attributes:
        transaction_id(Optional[int]): Primary key
        user_id (Optional[int]): Foreign key to User
        request_id(Optional[int]): Foreign key to Request
        created_at (datetime): Event creation timestamp
    """
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    request_id: Optional[int] = Field(default=None, foreign_key="request.request_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __str__(self) -> str:
        result = (f"Transaction id: {self.transaction_id}. User: {self.user.email}. Created at: {self.created_at}. Replenishment: {self.replenishment}. Decrease: {self.decrease}.")
        return result
    
    def __init__ (self) -> None:
        self.transaction_history = []

    def add_to_transaction_history(self, transaction: 'Transaction') -> None:
        """Добавляет запрос в список запросов пользователя."""
        self.transaction_history.append(transaction)
    
    def get_all_transactions(self):
        """Возвращает список всех запросов пользователя"""
        return self.transactions
    
class TransactionCreate(Transaction):
    """Schema for creating new transaction"""
    pass

User.Request = Relationship('Request', back_populates='User')
User.Transaction = Relationship('Transaction', back_populates='User')
User.Request_History = Relationship('Request History', back_populates='User')
User.Transaction_History = Relationship('Transaction History', back_populates='User')

class Admin(User):
    """
    Класс для представления администратора в системе.
    
    Attributes:
        administrator_rights(bool): Наличие прав администратора
    """
    def __init__(self, id, email, password, actual_balance, administrator_rights) -> None:
        super.__init__(id, email, password, actual_balance)
        self.administrator_rights = administrator_rights

    def change_user_balance(self, id, actual_balance):
         """Изменяет баланс отдельного пользователя"""
         change = input(int('Введите сумму, на которую необходимо изменить баланс. Если Вы хотите уменьшить баланс, введите сумму со знаком "-"'))
         self.actual_balance[id] += change