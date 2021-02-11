from string import Template
import random
from selenium import webdriver
from parsel import Selector
import time
import uuid
import os

mode = 1 # 1 - with add in file; 2 - with create file
system_name='msr' # systemname, see names of pattern files
profiles_count=10 # count of profiles whitch need create
file_format='.csv' # format output files

def generate_random_string(length):
    letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_random_numbers(length):
    letters = '123456789'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_random_fio(length):
    driver = webdriver.Chrome("c:/utils/chromedriver_win32/chromedriver.exe")
    # размер окна
    driver.set_window_size(1500, driver.get_window_size()['height'])
    docList = list()
    # get html by url вызываем метод get и передаем ему url сайта
    driver.get("http://mellarius.ru/random-inn")
    time.sleep(2)
    fioList = list(list())
    for i in range (0, length):
        driver.find_element_by_xpath("//div[@class='void__article']//button[@class='void__main_button15'][1]").click()
        fio = driver.find_element_by_xpath("//div[@class='void__article']//input[@id='fio']").get_attribute("value")
        fioList.append(fio.split(" "))
    driver.close()
    return fioList


def generate_random_doc(doc_type, count):
    driver = webdriver.Chrome("c:/utils/chromedriver_win32/chromedriver.exe")
    # размер окна
    driver.set_window_size(1500, driver.get_window_size()['height'])
    docList = list()
    # get html by url вызываем метод get и передаем ему url сайта
    driver.get("http://mellarius.ru/random-inn")
    time.sleep(2)
    for i in range (0, count):
        if doc_type == "snils":
            driver.find_element_by_xpath("//div[@class='void__article']//button[@class='void__main_button15'][8]").click()
            snils = driver.find_element_by_xpath("//div[@class='void__article']//input[@id='snils']").get_attribute("value")
            docList.append(snils)
        if doc_type == "inn":
            driver.find_element_by_xpath("//div[@class='void__article']//button[@class='void__main_button15'][3]").click()
            inn = driver.find_element_by_xpath("//div[@class='void__article']//input[@id='innfl']").get_attribute("value")
            docList.append(inn)
        if doc_type == "oms":
            driver.find_element_by_xpath("//div[@class='void__article']//button[@class='void__main_button15'][9]").click()
            oms = driver.find_element_by_xpath("//div[@class='void__article']//input[@id='oms']").get_attribute("value")
            docList.append(oms)
    driver.close()
    return docList

# create docLists
snilsList = list()
innList = list()
omsList = list()
fioList = list(list())

snilsList = generate_random_doc("snils", profiles_count)
innList = generate_random_doc("inn", profiles_count)
omsList = generate_random_doc("oms", profiles_count)
fioList = generate_random_fio(profiles_count)

# read pattern
with open('pattern_'+ system_name + '.txt', 'r', encoding="utf8") as f:
    pattern = ''.join(f.readlines())
t_pattern = Template(pattern)

try:
    os.mkdir("./datastorage/" + system_name)
except FileExistsError:
    pass

# create profiles and write on file
for i in range(0, profiles_count):
    data = dict(LastName0=fioList[i][0], FirstName0=fioList[i][1], MiddleName0=fioList[i][2],
                Birthday0=str(random.randint(10,29)) + ".0" + str(random.randint(1,9)) + "." + str(random.randint(1901,2020)), Snils0=snilsList[i], Oms0=omsList[i],
                Inn0=innList[i], SSO0=uuid.uuid4(), ESIA0=uuid.uuid4(), NUM8=generate_random_numbers(8))  # attrs support by pattern
    if mode == 1:
        with open("./datastorage/" + system_name + "/" + system_name + file_format, 'a+', encoding="utf8", newline='') as fp:
            fp.write('\n' + t_pattern.substitute(data))
    if mode == 2:
        with open("./datastorage/" + system_name + "/" + str(uuid.uuid4()) + file_format, 'w', encoding="utf8", newline='') as fp:
            fp.write(t_pattern.substitute(data))
