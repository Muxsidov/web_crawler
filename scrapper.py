from os import link
import requests
from bs4 import BeautifulSoup
import re

links_for_parsing = []

# Parsing all vacancies page (list of vacancies)
def parse_vacancies(request):
    vacancies_list = BeautifulSoup(request.content, 'html5lib')

    for i in vacancies_list.find_all('a', href=re.compile(r"/vakansy_view")):
        links_for_parsing.append(i["href"])
        #print(i["href"])

# Parsing vacancy_view (vacancy page itself)
def parse_vacancy_view(link):
    vacancy_view = BeautifulSoup(link.content, 'html5lib')
    
    # Useful to extract Job_title and Employer
    #print(vacancy_view.title.string)
    
    # Period of publication
    #print(vacancy_view.find(text="Period of publication"))
    
    # Search by CSS class td_sfera (td_grey_10 might be usefull too)
    temp = 0
    for i in vacancy_view.find_all(class_=re.compile("td_sfera")):
        #print(i.text)
        temp += 1
    
    if temp > 12:
        print(temp, vacancy_view.title)
    #print(vacancy_view.find_all(class_=re.compile("td_sfera")))

parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy.html"))
parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy-2.html"))
parse_vacancies(requests.get("https://uzjobs.uz/e/vakansy-3.html"))

#print(links_for_parsing)
print(len(links_for_parsing))

#request = requests.get("https://uzjobs.uz/r/vakansy_view-27452.html")
for i in links_for_parsing:
    parse_vacancy_view(requests.get("https://uzjobs.uz/" + i))