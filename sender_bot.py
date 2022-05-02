import psycopg2
from psycopg2 import OperationalError
import requests
import telebot

tg_token = "5377110236:AAHy2nS-91j_IbSo5A0Zru1PhJMsNICzu-A"
tel_group_id = "-1001696534045"

# Creating connection to PostgreSQL
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect( 
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred while connecting")
    return connection

# Connecting to database
connection = create_connection(
    "vacancies", "postgres", "postgres", "127.0.0.1", "5432"
)

# Selecting Records
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

select_vacancies = "SELECT * FROM vacancies"
vacancies = execute_read_query(connection, select_vacancies)

# Send a message to telegram channel
def send_to_telegram(message):
    try:
     telegram_api_url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tel_group_id}&text={message}"
     tel_resp = requests.get(telegram_api_url)
    except Error as e:
        print(f"While sending the message to tg '{e}' occurred")

for vacancy in vacancies:
    vacancy = str(vacancy).replace("&", "and")
    send_to_telegram(vacancy)
