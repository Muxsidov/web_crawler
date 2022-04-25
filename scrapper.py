from asyncio.windows_events import NULL
from os import link
from matplotlib.pyplot import title
import requests
from bs4 import BeautifulSoup
import re
import psycopg2
from psycopg2 import OperationalError

links_for_parsing = []

# List of job descriptions
vacacies_list = []

# Parsing all vacancies page (list of vacancies)
def parse_vacancies(request):
    vacancies_list = BeautifulSoup(request.content, 'html5lib')

    for i in vacancies_list.find_all('a', href=re.compile(r"/vakansy_view")):
        links_for_parsing.append(i["href"])
        #print(i["href"])

# Parsing vacancy_view (vacancy page itself)
def parse_vacancy_view(link):
    vacancy_view = BeautifulSoup(link.content, 'html5lib')
    
    single_vacancy = []
    # Useful to extract Job_title and Employer
    #print(vacancy_view.title.string)
    
    # Job title
    title = vacancy_view.find(class_=re.compile("h2_grey"))
    single_vacancy.append(title.text)
    #print(title.text)

    # Employer
    employer = vacancy_view.find('a', href=re.compile(r"/company_view"))
    single_vacancy.append(employer.text)
    #print(employer.text)

    # Period of publication
    #print(vacancy_view.find(text="Period of publication"))

    #for i in vacancy_view.find_all(class_=re.compile("td_grey")):
        #print(i)
        #print(i.text)
    
    # Search by CSS class td_sfera (td_grey_10 might be usefull too)
    temp = 0
    for i in vacancy_view.find_all(class_=re.compile("td_sfera")):
        single_vacancy.append(i.text)
        #print(i.text)
        temp += 1
    
    if temp < 13:
        single_vacancy.insert(11, None)
    # if temp > 12:
    #     print(temp, vacancy_view.title)
    #     print(vacancy_view.find_all(class_=re.compile("td_sfera")))
    print(len(single_vacancy))
    vacacies_list.append(tuple(single_vacancy))

parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy.html"))
parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy-2.html"))
parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy-3.html"))

#print(links_for_parsing)
print(len(links_for_parsing))

#request = requests.get("https://uzjobs.uz/r/vakansy_view-27452.html")
# for i in links_for_parsing:
#     parse_vacancy_view(requests.get("https://uzjobs.uz/" + i))
parse_vacancy_view(requests.get("https://uzjobs.uz/e/vakansy_view-27529.html"))

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

# Create Database on PostgreSQL
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
"""
create_database_query = "CREATE DATABASE vacancies"
create_database(connection, create_database_query)
"""
# Connecting to database
connection = create_connection(
    "vacancies", "postgres", "postgres", "127.0.0.1", "5432"
)

# Execute Python SQL queries on PostgreSQL
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# Query for creating the tables
create_users_table = """
CREATE TABLE IF NOT EXISTS vacancies (
  id SMALLSERIAL,
  job_title TEXT NOT NULL, 
  employer TEXT NOT NULL,
  publication_period TEXT,
  position TEXT NOT NULL,
  duties TEXT,
  age TEXT,
  gender TEXT,
  residence TEXT,
  education TEXT,
  requirements TEXT,
  region TEXT,
  employment TEXT,
  salary TEXT NOT NULL,
  motivation TEXT,
  information TEXT
)
"""

execute_query(connection, create_users_table)

vacancy_records = ', '.join(["%s"] * len(vacacies_list))

# Inserting into "vacancies db"
insert_query = (
    f"INSERT INTO vacancies (job_title, employer, publication_period, position, duties, age, gender, residence, education, requirements, region, employment, salary, motivation, information) VALUES {vacancy_records} RETURNING id" 
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, vacacies_list)
