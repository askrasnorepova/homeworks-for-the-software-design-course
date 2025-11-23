from dataclasses import dataclass, field
from typing import List
from pydub import AudioSegment
import re
import magic
import math


@dataclass
class User:
    """
    Класс для представления пользователя в системе.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Пароль пользователя
        actual_balance(float): Текущий баланс
    """

    id: int
    email: str
    password: str
    actual_balance: float

    def __post_init__(self) -> None:
        self._validate_email()
        self._validate_password()

    def _validate_email(self) -> None:
        """Проверяет корректность email."""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self) -> None:
        """Проверяет минимальную длину пароля."""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

@dataclass

class Request:
    """
    Класс запросов пользователя на расшифровку аудиозаписи

    Attributes:
        audio(str): путь к файлу с аудиозаписью
        duration(float): длительность аудиозаписи
        cost(float): стоимость запроса
        request_history (list['Request']): История запросов пользователя
    """

    audio: str
    duration: float
    cost: float
    request_history: List['Request'] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_request()

    def _validate_request(self) -> None:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(audio)
        if 'audio' not in file_type:
            raise ValueError("Invalid request format. Please upload audio")
        
    def get_duration(self, audio) -> None:
        audio_file = AudioSegment.from_file(audio)
        dur_audio = audio_file.duration_seconds
        return dur_audio

    def get_price(self, cost) -> None:
        duration_audio = self.get_duration()
        price = math.ceil(duration_audio / cost)
        return price
    
    def add_to_request_history(self, request: 'Request') -> None:
        """Добавляет запрос в список запросов пользователя."""
        self.append(request)

@dataclass
class Model:
    """
    Класс для вызова модели
    
    Attributes:
        model (str): путь к размещению модели
    """
    model: str

    def use_model(self) -> None:
        return model(audio)

@dataclass
class Transaction:
    """ Класс для представления финансовых операций пользователя

    Attributtes:
        actual_balance(float): Текущий баланс
        replenishment (float): Сумма пополнения
        decrease (float): Сумма списания за запрос
        transaction_history (list['Transaction']): История транзакций пользователя
    """

    replenishment: float
    decrease: float
    transaction_history: (list['Transaction']) = field(default_factory=list)

    def replenish_balance(self, replenishment, transaction: 'Transaction') -> None:
        """Пополняет баланс пользователя"""
        actual_balance += replenishment
        transaction = replenishment
        return f"Ваш баланс пополнен на {replenishment} кр. На Вашем счете: {actual_balance} кр."
    
    def decrease_balance(self) -> None:
        """Списание средств за новый запрос"""
        req = Request
        decrease = req.get_price()
        actual_balance -= decrease
        return f"С Вашего счета списано {decrease} кр. На Вашем счете: {actual_balance} кр."
    
    def add_to_transaction_history(self, transaction: 'Transaction') -> None:
        """Добавляет запрос в список запросов пользователя."""
        self.append(Transaction)

@dataclass
class Admin(User):
    """
    Класс для представления администратора в системе.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Пароль пользователя
        actual_balance(float): Текущий баланс
        administrator_rights(bool): Наличие прав администратора
    """
    def __init__(self, id, email, password, actual_balance, administrator_rights) -> None:
        super.__init__(id, email, password, actual_balance)
        self.administrator_rights = administrator_rights

    def change_user_balance(self, id, actual_balance):
         change = input('Введите сумму, на которую необходимо изменить баланс')
         self.actual_balance[id] += change