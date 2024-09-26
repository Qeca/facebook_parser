import json
import time
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def click_see_more_buttons(driver: webdriver.Chrome) -> None:
    try:
        see_more_buttons = driver.find_elements(By.XPATH,
                                                "//div[contains(text(), 'Ещё') or contains(text(), 'See More')]")
        for button in see_more_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1.5)
            except Exception as e:
                pass
    except Exception as e:
        pass


def get_post_data(page_source: str, posts_data: List[Dict[str, Any]]) -> None:
    soup = BeautifulSoup(page_source, 'lxml')

    posts = soup.find_all('div', class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

    for post in posts:
        post_data: Dict[str, Any] = {}

        post_message_1 = post.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a')
        if post_message_1:
            post_data['main_message'] = post_message_1.text

        post_messages = post.find_all('div', class_='x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a')
        post_data['additional_messages'] = [message.text for message in post_messages]

        post_photos: List[Dict[str, str]] = []
        post_photo_span = post.find_all('div', class_="x10l6tqk x13vifvy")
        for photo_span in post_photo_span:
            img_tag = photo_span.find('img')
            if img_tag:
                descr_photo = img_tag.get('alt')
                photo_link = img_tag.get('src')
                post_photos.append({'description': descr_photo, 'photo_link': photo_link})

        post_data['photos'] = post_photos
        if post_data not in posts_data:
            posts_data.append(post_data)
            print(post_data)


def parse_posts(n: int, driver_start: webdriver.Chrome) -> None:
    time.sleep(1)
    posts_data: List[Dict[str, Any]] = []
    i = 0
    scroll_position = 0
    no_new_posts_count = 0
    max_no_new_posts_iterations = 5

    while len(posts_data) < n and no_new_posts_count < max_no_new_posts_iterations:
        previous_post_count = len(posts_data)

        driver_start.execute_script(f"window.scrollTo({scroll_position}, {scroll_position + 5000});")
        time.sleep(3)

        click_see_more_buttons(driver_start)

        page_source = driver_start.page_source

        print(f"Итерация {i + 1}")
        get_post_data(page_source, posts_data)
        print(f"Всего собрано постов: {len(posts_data)}")

        if len(posts_data) == previous_post_count:
            no_new_posts_count += 1
        else:
            no_new_posts_count = 0

        scroll_position += 5000
        i += 1

    with open('../../Desktop/posts_data.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=4)

    driver_start.quit()
