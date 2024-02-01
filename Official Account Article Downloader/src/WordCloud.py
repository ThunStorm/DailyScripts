import jieba
import wordcloud
import matplotlib.pyplot as plt
import imageio
import re


def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    return emoji_pattern.sub('', text)


def remove_html(text):
    cleanr = re.compile('<.*?>')  # 定义要删除的标记模式
    cleaned = re.sub(cleanr, '', text)  # 使用re.sub()函数进行替换操作

    return cleaned

# 读取文件
words = ""
articles = ["#上海", "#现实和理想", "#个人成长", "#人情世故", "#山宝在等你", "#成年人"]
for article in articles:
    filename = r'articles/' + article + '.txt'
    with open(filename, "r", encoding='utf-8') as f:
        words = words + f.read()

print("有空格", len(words))
words = words.replace(" ", "")
print("无空格1", len(words))
words = remove_emojis(words)
print("无emoji", len(words))
words = remove_html(words)
print("无html", len(words))
jieba.del_word("正文")  # 结巴词库切分词
jieba.del_word("标题")  # 结巴词库切分词
jieba.del_word("发布")  # 结巴词库切分词
jieba.del_word("时间")  # 结巴词库切分词
# word_list = jieba.del_word("自己")  # 结巴词库切分词
word_list = jieba.cut(words, cut_all=False)  # 结巴词库切分词
word_list = [word for word in word_list if len(word.strip()) > 1]  # 清洗一个字的词
word_clean = " ".join(word_list)
# """
mask = imageio.v3.imread("./resources/tao2.jpg")
wc = wordcloud.WordCloud(font_path="simkai.ttf",  # 指定字体类型
                         background_color="white",  # 指定背景颜色
                         max_words=500,  # 词云显示的最大词数
                         max_font_size=500,
                         width=1000, height=1000,
                         mask=mask)  # 指定模板
wc = wc.generate(word_clean)  ##生成词云
wc.to_file("wordcloud.png")  # 保存图片
plt.imshow(wc)
plt.axis("off")
plt.show()
# """

"""Wordcloud详细参数设置
def __init__(self, font_path=None, width=400, height=200, margin=2,
    ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
    color_func=None, max_words=200, min_font_size=4,
    stopwords=None, random_state=None, background_color='black',
    max_font_size=None, font_step=1, mode="RGB",
    relative_scaling='auto', regexp=None, collocations=True,
    colormap=None, normalize_plurals=True, contour_width=0,
    contour_color='black', repeat=False,
    include_numbers=False, min_word_length=0):
"""
