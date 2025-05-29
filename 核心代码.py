from bs4 import BeautifulSoup
import requests
import os

# 请求URL
url = "https://www.ireader.com/index.php?ca=Chapter.Index&pca=bookdetail.index&bid=1023955&cid=11"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 提取书名
book_title = soup.select_one('i a').get_text().strip()

# 创建文件夹
os.makedirs(book_title, exist_ok=True)

# 提取文章内容
article = soup.find('div', class_='article')
title = article.find('h2').get_text().strip()
paragraphs = [p.get_text().strip() for p in article.find_all('p')]

# 保存文件
with open(f"{book_title}/{title}.txt", 'w', encoding='utf-8') as f:
    f.write("\n".join(paragraphs))