import psycopg2
from psycopg2 import OperationalError
import requests
import telebot
import time

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

select_job_titles = "SELECT job_title FROM vacancies"
job_titles = execute_read_query(connection, select_job_titles)

# Send a message to telegram channel
def send_to_telegram(message):
    try:
     telegram_api_url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tel_group_id}&text={message}"
     tel_resp = requests.get(telegram_api_url)
    except Error as e:
        print(f"While sending the message to tg '{e}' occurred")

# Call send_to_telegram for each vacancy
count = 38
while count != 83:
    for vacancy in vacancies:  
        if vacancy[0] == count:
            print(vacancy[0], vacancy[1])
            #vacancy = str(vacancy).replace("&", "and")
            send_to_telegram(vacancy)
            count += 1
            time.sleep(2)

# Remove unwanted characters from the message
# characters = "'()"
# #print(type(job_titles))
# for job_title in job_titles:
#     for char in characters:
#         job_title = str(job_title).replace(char, "")
#     print(job_title)
# print(len(job_titles))

