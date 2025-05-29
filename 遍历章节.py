from bs4 import BeautifulSoup
import requests
import os

# 基础URL（不包含cid参数）
base_url = "https://www.ireader.com/index.php?ca=Chapter.Index&pca=bookdetail.index&bid=1023955&cid="

# 请求第一页获取书名
response = requests.get(base_url + "1")
response.raise_for_status()  # 如果请求失败直接抛出异常
soup = BeautifulSoup(response.text, 'html.parser')

# 提取书名
book_title = soup.select_one('i a').get_text().strip()

# 创建文件夹
os.makedirs(book_title, exist_ok=True)

# 设置最大页数（根据需要调整）
max_pages = 10

# 循环下载多个章节
for page in range(1, max_pages + 1):
    # 构建当前页URL
    url = base_url + str(page)
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败直接抛出异常
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取文章内容（如果找不到直接报错）
    article = soup.find('div', class_='article')
    if not article:
        raise Exception(f"第 {page} 页未找到文章内容")
    
    # 提取章节标题（如果找不到直接报错）
    title_tag = article.find('h2')
    if not title_tag:
        raise Exception(f"第 {page} 页未找到标题")
    
    chapter_title = title_tag.get_text().strip()
    
    # 提取正文内容
    paragraphs = [p.get_text().strip() for p in article.find_all('p')]
    content = "\n".join(paragraphs)
    
    # 保存文件
    with open(f"{book_title}/{chapter_title}.txt", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已保存第 {page} 页: {chapter_title}")
