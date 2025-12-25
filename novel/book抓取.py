import random

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

from selenium.webdriver.support.wait import WebDriverWait


def save_data(data, file_name):
    """
     将数据保存到指定的CSV文件中。

     参数:
     data (list of tuple): 包含数据的列表，每个元素是一个包含数据字段的元组。
     file_name (str): 要保存到的文件名。

     返回:
     无
     """
    pd_data = pd.DataFrame(data,
                           columns='书名 作者 分类 简介 字数 状态 图片链接'.split())
    if not os.path.exists(file_name): # 如果文件不存在
        # 写第一页
        pd_data.to_csv(file_name,
                       header=True,
                       index=False,
                       encoding='utf-8-sig')
    else:
        # 写其余页
        pd_data.to_csv(file_name,
                       header=False,    # 不写列名
                       index=False,
                       encoding='utf-8-sig',
                       mode = 'a+') # 追加内容

# 获取一个小说的数据
def get_one_novel(novel):
    name = novel.find_element(By.CSS_SELECTOR, '.book-info>h3>a').text.strip()

    author = novel.find_element(By.CSS_SELECTOR, '.book-info>h4>a').text.strip()

    category = novel.find_element(By.CSS_SELECTOR, '.book-info>p.tag>span.org').text.strip()

    info = novel.find_element(By.CSS_SELECTOR, '.book-info>p.intro').text.strip()

    # 字数
    words = novel.find_element(By.CSS_SELECTOR, '.book-info>p.tag>span.blue').text.strip()

    state = novel.find_element(By.CSS_SELECTOR, '.book-info>p.tag>span.pink').text.strip()

    image_link = novel.find_element(By.CSS_SELECTOR, '.book-img>a>img').get_attribute('src')
    return (name, author, category, info, words, state, image_link)

# 获取所有小说的数据
def get_all_novels(driver):
    # 添加显式等待确保容器加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.right-book-list'))
    )
    # 定位小说容器
    novel_elements = driver.find_element(By.CSS_SELECTOR, '.right-book-list')
    novel_element = novel_elements.find_elements(By.CSS_SELECTOR, '.right-book-list>ul>li') # len(novel_element)
    print(f"共找到{len(novel_element)}本小说")
    data = [get_one_novel(novel) for novel in novel_element]
    return data

# 下载图片
def download_pic(name, image_link):
    response = requests.get(image_link, timeout=10)
    response.raise_for_status()
    # 获取文件类型
    content_type = response.headers.get('Content-Type', '')
    type = content_type.split('/')[-1]
    if type not in ['jpeg', 'png', 'jpg', 'webp']:
        type = 'jpg'
    folder_path = "photo"
    pics_name = os.path.join(folder_path, f'{name}.{type}')
    os.makedirs(folder_path, exist_ok=True)
    with open(pics_name, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    url = r'https://www.hongxiu.com/category'
    driver = webdriver.Edge()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到浏览器底部
    time.sleep(2)

    current_page = 1
    while True:
        try:
            current_data = get_all_novels(driver)
            save_data(current_data, 'books.csv')
            print(f"已保存第 {current_page} 页数据")
            # # 保存图片数据
            # for novel_info in current_data:
            #     name = novel_info[0]  # 书名是元组第一个元素
            #     image_link = novel_info[6]  # 图片链接是第六个元素
            #     download_pic(name, image_link)
            # 定位下一页按钮（排除禁用状态）
            delay = random.uniform(5, 10)
            time.sleep(delay)
            next_buttons = driver.find_elements(
                By.CSS_SELECTOR, ".lbf-pagination-next:not(.lbf-pagination-disabled)"
            )

            if not next_buttons:
                print("已到达最后一页，终止抓取")
                break
                # 点击下一页
            driver.execute_script("arguments[0].click();", next_buttons[0])
            # 抓取当前页数据
            current_page += 1
            time.sleep(random.uniform(1, 2))  # 随机短延迟

        except Exception as e:
            print(f"翻页失败: {str(e)}")
            break

