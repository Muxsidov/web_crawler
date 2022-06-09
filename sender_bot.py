from ssl import VERIFY_X509_PARTIAL_CHAIN
from tkinter import EXCEPTION
from matplotlib.pyplot import text
import psycopg2
from psycopg2 import OperationalError
import requests
import telebot
import time
from urllib.parse import quote

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

select_vacancies = f"SELECT * FROM vacancies WHERE status = 0 and id = 1"
vacancies = execute_read_query(connection, select_vacancies)

# send_to_telegram(vacancies)
def send_to_telegram(message, id):
    try:
        print(id)
        # https://stackoverflow.com/questions/6431061/python-encoding-characters-with-urllib-quote
        # vacancies = quote(str(vacancies).encode("utf-8"))
        print(quote(message))
        print(type(message))
        telegram_api_url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tel_group_id}&text={quote(message)}"
        # for messages being too long https://stackoverflow.com/questions/70819525/send-long-message-in-telegram-bot-python
        tel_resp = requests.get(telegram_api_url)
        print("message has been sent sucesfully")
        # vacancies = execute_read_query(connection, f"UPDATE vacancies SET status = 1 WHERE id = {i}")
        # return True
    except Exception as e:
        print(f"While sending the message to tg '{e}' occurred")

for vacancy in vacancies:  
    (id, status, job_title, employer, publication_period, position, duties, age, gender, residence, education, requirements, region, employment, salary, motivation, *information) = vacancy
    text = f"{job_title}\n{employer}\n{publication_period}\n{position}\n{duties}\n{age}\n{gender}\n{residence}\n{education}\n{requirements}\n{region}\n{employment}\n{salary}\n{motivation}\n{information}\n"
    print("text: ", text)
    send_to_telegram(text, id)

