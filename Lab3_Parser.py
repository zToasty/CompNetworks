3mport time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Константы
BASE_URL = "https://novosibirsk.e2e4online.ru/"
CSV_FILENAME = "videocards.csv"


# Инициализация драйвера
service = Service(executable_path=r'./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Запись заголовков в CSV файл
with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название", "Цена (₽)", "Бонусы", "Описание"])


def scrape_page():
    try:
        container = driver.find_element(By.CLASS_NAME, "subcategory-new-offers__offers")
        cards = container.find_elements(By.CLASS_NAME, "block-offer-item.subcategory-new-offers__item-block")

        for card in cards:
            try:
                name_class = 'block-offer-item__name'
                name = card.find_element(By.CLASS_NAME, name_class).text.strip()

                price_class = 'price-block__price'
                price = card.find_element(By.CLASS_NAME, price_class).text.strip().replace("₽", "").replace(" ", "")

                try:
                    description_class = 'block-offer-item__description.lg-and-up'
                    description = card.find_element(By.CLASS_NAME, description_class).text.strip()
                except NoSuchElementException:
                    description = "Нет описания"

                try:
                    bonuses_class = 'offer-bonus-info-item__bonus-count-text._label'
                    bonuses = card.find_element(By.CLASS_NAME, bonuses_class).text.strip().replace("Б", "").replace("+","").replace(" ","")
                except NoSuchElementException:
                    bonuses = "0"

                with open(CSV_FILENAME, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([name, price, bonuses, description])
                
                print(f"Собрано: {name} | {price} ₽ | {bonuses} бонусов | {description}")

            except Exception as e:
                print(f"Ошибка при парсинге товара: {e}")
               
    except Exception as e:
        print(f"Ошибка загрузки страницы: {e}")


def scrape_all_pages():
    driver.get(BASE_URL)
    page = 1
    
    # Принятие геолокации
    geo_yes_button = driver.find_element(By.CSS_SELECTOR, 'button.geolocation-confirm__confirm-button')
    geo_yes_button.click()

    # Поиск видеокарт
    search_field = driver.find_element(By.CSS_SELECTOR, 'input.e2e4-uikit-field__input')
    search_field.clear()
    search_field.send_keys("Видеокарта RTX")
    search_field.send_keys("\n")

    time.sleep(2)

    # Закрытие уведомления
    close_notification = driver.find_element(By.CSS_SELECTOR, 'button.onboarding-block__btn-close')
    close_notification.click()

    time.sleep(4)

    while True:
        print(f"Собираем страницу {page}...")

        try:
            scrape_page()
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
            break

        try:
            next_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="На следующую страницу"]'))
            )
            next_button.click()
            time.sleep(2)  # Пауза для загрузки
            page += 1
        except TimeoutException:
            print("Страницы закончились.")
            break


scrape_all_pages()

# Закрытие браузера
driver.quit()
print("Парсинг завершен!")
