from database.config import get_settings
from database.database import get_session, init_db, get_database_engine
from sqlmodel import Session
from models.description import *


if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.API_VERSION)
    print(f'Debug: {settings.DEBUG}')
    
    print(settings.DB_HOST)
    print(settings.DB_NAME)
    print(settings.DB_USER)
    
    init_db(drop_all=True)
    print('Init db has been success')
    
    test_user = User(email='test1@gmail.com', password='test')
    test_user_2 = User(email='test2@gmail.com', password='test')
    test_user_3 = User(email='test3@gmail.com', password='test')
    
    test_request = Request(audio='test')
    test_request_2 = Request(audio='test')

    test_transaction = Transaction(actual_balance=100, replanishment = 35, decrease = 0)
    test_transaction_2 = Transaction(actual_balance=150, replanishment = 0, decrease = 28.5)
    test_transaction_3 = Transaction(actual_balance=120, replanishment = 10, decrease = 0)
    
    test_user.requests.append(test_request)
    test_user.requests.append(test_request_2)

    test_user_2.transactions.append(test_transaction)
    test_user_3.transactions.append(test_transaction_2)
    test_user.transactions.append(test_transaction_3)
    
    engine = get_database_engine()
    
    with Session(engine) as session:
        create_user(test_user, session)
        create_user(test_user_2, session)
        create_user(test_user_3, session)
        users = get_all_users(session)
        
    print('-------')
    print(f'Id локального пользователя: {id(test_user)}')
    print(f'Id пользователя из БД: {id(users[0])}')
    print(f'Id одинаковые: {id(test_user) == id(users[0])}')

    print('-------')
    print('Пользователи из БД:')        
    for user in users:
        print(user)
        print('Пользовательские запросы:')
        print('Баланс пользователя:', actual_balance)
        
    print('История запросов:')
    for user in users:
        print(user)
        print(get_all_requests(user.id))
        
