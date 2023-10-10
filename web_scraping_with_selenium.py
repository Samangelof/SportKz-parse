from selenium import webdriver
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urldefrag

# Определите URL страницы, которую вы хотите скрапить, и имя выходного файла здесь
base_url = 'https://diapazon.kz/category/sport/aktobe/'
output_file = 'parsed_data.json'

# URL для скрапинга страницы
url = 'https://diapazon.kz/category/sport/aktobe/'


def get_page_source(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source


def get_links_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    links_data = []
    
    links = soup.find_all('li', class_='news-box__item news-cart')  # Находим все элементы списка с классом 'news-box__item news-cart'
    
    for link_item in links:
        link = link_item.find('a', href=True)  # Находим ссылку внутри элемента списка
        if link:
            href = link['href']  # Получаем значение атрибута 'href' ссылки
            text = link.find('span', class_='news-cart__name link').text.strip()  # Извлекаем текст ссылки
            time_div = link_item.find('div', class_='news-cart__meta-row')  # Находим div с временем
            if time_div:
                time = time_div.find('time', class_='news-cart__pub-time').text.strip()  # Извлекаем время
            else:
                time = None
            links_data.append({'href': urljoin(base_url, urldefrag(href).url), 'text': text, 'time': time})  # Добавляем данные в список
    
    return links_data


def get_all_links(base_url, num_pages=3):
    all_links_data = []  # Создаем список для хранения всех данных о ссылках
    
    for page_num in range(1, num_pages + 1):
        url = f'{base_url}?page={page_num}'  # Формируем URL с номером страницы
        page_source = get_page_source(url)
        links_data = get_links_data(page_source)  # Извлекаем ссылки с текущей страницы
        
        if not links_data:
            break  # Если не удалось найти ссылки на странице, выходим из цикла
        
        all_links_data.extend(links_data)  # Добавляем данные о ссылках к общему списку
    
    return all_links_data


def main():
    all_links_data = get_all_links(base_url)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(all_links_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Данные сохранены в файл: {output_file}")


if __name__ == "__main__":
    main()
