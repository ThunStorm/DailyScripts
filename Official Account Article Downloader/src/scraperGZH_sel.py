from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

URL = {
    "tag:个人成长": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=2251906292149731330",
    "tag:山宝在等你": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=1760489790744903680",
    "tag:上海": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=2041197632894615555",
    "tag:人情世故": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=2107498587021459460",
    "tag:成年人": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=1702324076343541762",
    "tag:现实和理想": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=1801834405804457986"}


def scroll_to_bottom(driver, scroll_amount):
    for _ in range(scroll_amount):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def get_links(page_source):
    # 使用BeautifulSoup解析页面源代码
    soup = BeautifulSoup(page_source, 'html.parser')
    # 假设链接包含在<a>标签内，并且这些<a>标签位于某个列表元素中，如<ul>或<ol>
    # 我们将查找所有的<ul>和<ol>标签，然后遍历其中的<li>标签来找到<a>标签
    link_texts = []
    for list_element in soup.find_all('ul'):
        for li in list_element.find_all('li', class_='album__list-item js_album_item js_wx_tap_highlight wx_tap_cell'):
            # 查找<li>标签内的<a>标签
            link_text = li.get('data-link').strip()
            link_texts.append(link_text)
    return link_texts


def articles_link_finder(url):
    # 初始化Chrome WebDriver（确保你已经安装了Chrome和对应的chromedriver）
    driver = webdriver.Chrome()
    # 设置窗口大小（可选）
    driver.set_window_size(1024, 768)
    # 导航到目标网页
    driver.get(url)
    # 滚动次数（根据页面动态加载的情况调整）
    scroll_times = 8
    # 循环滚动页面以加载更多内容
    scroll_to_bottom(driver, scroll_times)
    # 等待页面完全加载（根据网络状况和页面加载时间调整）
    time.sleep(3)
    # 获取页面源代码
    page_source = driver.page_source
    # 获取文章链接集
    link_texts = get_links(page_source)
    # 关闭WebDriver
    driver.quit()
    return link_texts


def get_article(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    title = soup.find('h1', class_='rich_media_title').text.strip()
    publish_time = soup.find('em', id='publish_time').text.strip()
    # article_text = soup.find_all('span', attrs={'style': re.compile(r'(.*visibility: visible;.*) | (.*font-size.*)')})
    article_text = soup.find_all(lambda tag: tag.get('style') and not tag.get('href') and (
            'visibility: visible;' in tag.get('style') or 'font-size' in tag.get('style')))
    article = "".join([text.text.replace('\u200d', ' ').strip() for text in article_text]).strip()
    return f'标题：{title}\n发布时间：{publish_time}\n正文：{article}\n\n'


def get_article_text(url):
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 768)
    driver.get(url)
    scroll_times = 3
    scroll_to_bottom(driver, scroll_times)
    time.sleep(2.5)
    page_source = driver.page_source
    article_text = get_article(page_source)
    driver.quit()
    return article_text


# 主程序
for (tag, url) in URL.items():
    link_texts = articles_link_finder(url)
    # # 打印提取到的链接文本
    print("#" + tag[4:] + "：共有 " + str(len(link_texts)) + " 篇文章")
    for _ in range(len(link_texts)):
        article_text = get_article_text(link_texts[_])
        filename = "#" + tag[4:] + ".txt"
        with open(filename, "a", encoding='utf-8') as f:
            f.write(article_text)
        print("第 " + str(_) + " 篇文章\n" + article_text)
