import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def open_wikipedia_page(query):
    # Формируем URL на основе запроса пользователя
    base_url = "https://ru.wikipedia.org/wiki/"
    query_url = base_url + query.replace(" ", "_")

    # Настройка WebDriver
    browser = webdriver.Firefox()

    try:
        # Переходим на сформированный URL
        browser.get(query_url)
        time.sleep(2)  # Ожидаем загрузки страницы

        while True:
            # Меню действий
            choice = input(
                "\nВыберите действие:\n1. Листать параграфы\n2. Перейти на случайную связанную страницу\n3. Выйти\nВведите номер: ")

            if choice == "1":
                # Листаем параграфы текущей статьи
                paragraphs = [p.text for p in browser.find_elements(By.TAG_NAME, 'p') if p.text.strip()]
                for paragraph in paragraphs:
                    print(paragraph)
                    if input("Нажмите Enter для следующего параграфа или введите 'exit', чтобы вернуться: ").lower() == 'exit':
                        break

            elif choice == "2":
                # Переход на случайную связанную страницу
                linked_divs = browser.find_elements(By.TAG_NAME, 'div')
                links = []
                for div in linked_divs:
                    a_tags = div.find_elements(By.TAG_NAME, 'a')
                    for a in a_tags:
                        href = a.get_attribute('href')
                        if href and '/wiki/' in href:
                            links.append(a)

                if links:
                    # Выбираем случайную ссылку из списка
                    random_link = random.choice(links)
                    print(f"Переходим на страницу: {random_link.text} ({random_link.get_attribute('href')})")
                    browser.get(random_link.get_attribute('href'))
                    time.sleep(2)
                else:
                    print("Связанные страницы не найдены.")

            elif choice == "3":
                break

            else:
                print("Некорректный выбор, попробуйте снова.")

    finally:
        browser.quit()

# Запрос у пользователя на первоначальный запрос
initial_query = input("Введите запрос для поиска на Википедии: ")
open_wikipedia_page(initial_query)