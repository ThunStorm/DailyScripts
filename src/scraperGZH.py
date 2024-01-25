import requests
from bs4 import BeautifulSoup


def extract_link_texts(url):
    # 发送HTTP GET请求
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"请求网页时出错: {e}")
        return []

        # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 假设链接包含在<a>标签内，并且这些<a>标签位于某个列表元素中，如<ul>或<ol>
    # 我们将查找所有的<ul>和<ol>标签，然后遍历其中的<li>标签来找到<a>标签
    link_texts = []
    for list_element in soup.find_all('ul'):
        for li in list_element.find_all('li', class_='album__list-item js_album_item js_wx_tap_highlight wx_tap_cell'):
            # 查找<li>标签内的<a>标签
            link_text = li.get('data-link').strip()
            link_texts.append(link_text)
    return link_texts


# 示例用法
url = ('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNTkyNTU2NQ==&action=getalbum&album_id=2251906292149731330'
       '&scene=126&sessionid=1049317723&uin=&key=&devicetype=Windows+11+x64&version=63090819&lang=zh_CN&ascene=0')  #
link_texts = extract_link_texts(url)
print(len(link_texts))
# for text in link_texts:
#     print(text)
