# 导入所需模块
from bs4 import BeautifulSoup  # HTML解析
import requests, os  # HTTP请求和文件操作

# 书籍基础URL（cid参数表示章节ID）
base_url = "https://www.ireader.com/index.php?ca=Chapter.Index&pca=bookdetail.index&bid=1023955&cid="

# 获取第一章内容并提取书名
r = requests.get(base_url + "1")
book_title = BeautifulSoup(r.text, 'html.parser').select_one('i a').get_text()  # 从i>a标签提取书名
os.makedirs(book_title, exist_ok=True)  # 创建书名目录
print(f"书名：{book_title}\n")

# 章节计数器
page = 1

# 循环下载所有章节
while True:
    # 获取并解析当前章节HTML
    soup = BeautifulSoup(requests.get(base_url + str(page)).text, 'html.parser')
    
    # 查找文章内容区域和标题（找不到则退出循环）
    if not (article := soup.find('div', class_='article')) or not (title := article.find('h2')): 
        break
    
    # 保存章节内容到文本文件
    title = title.get_text()
    with open(f"{book_title}/{title}.txt", 'w') as f:
        # 提取所有段落内容并连接为文本
        f.write("\n".join(p.get_text() for p in article.find_all('p')))
    
    # 打印进度
    print(f"{page} 标题：{title}")
    page += 1  # 下一章

# 完成提示
print("所有章节下载完成")
