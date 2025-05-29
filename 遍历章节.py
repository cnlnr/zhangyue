# 导入必要的库
from bs4 import BeautifulSoup  # HTML解析库
import requests  # HTTP请求库
import os  # 操作系统接口库

# 定义基础URL（不包含章节ID参数）
base_url = "https://www.ireader.com/index.php?ca=Chapter.Index&pca=bookdetail.index&bid=1023955&cid="

# 获取第一页内容用于提取书名
response = requests.get(base_url + "1")  # 请求第一章内容
response.raise_for_status()  # 检查请求是否成功（HTTP状态码200）
soup = BeautifulSoup(response.text, 'html.parser')  # 解析HTML内容

# 提取书名（通过CSS选择器定位书名元素）
book_title = soup.select_one('i a').get_text().strip()  # 从<i>标签内的<a>标签获取文本
os.makedirs(book_title, exist_ok=True)  # 创建以书名为名的文件夹（如果已存在则忽略）

# 初始化页码计数器
page = 1
while True:  # 无限循环直到没有新章节
    # 构建当前章节URL
    url = base_url + str(page)
    response = requests.get(url)  # 获取章节页面
    response.raise_for_status()  # 确保请求成功
    
    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找文章内容区域（使用class选择器）
    article = soup.find('div', class_='article')
    # 在文章区域内查找标题（h2标签）
    title_tag = article.find('h2') if article else None
    
    # 检查是否找到内容和标题
    if not article or not title_tag:
        break  # 如果找不到内容或标题，退出循环
    
    # 获取标题文本并清理空格
    title_text = title_tag.get_text().strip()
    # 构建文件路径：书名/章节标题.txt
    file_path = os.path.join(book_title, f"{title_text}.txt")
    
    # 提取所有段落文本（<p>标签内容）
    paragraphs = [p.get_text().strip() for p in article.find_all('p')]
    # 用换行符连接段落
    content = "\n".join(paragraphs)
    
    # 写入文件（UTF-8编码）
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 显示进度信息
    print(f"已保存第 {page} 页: {title_text}")
    page += 1  # 页码递增，准备获取下一章

# 完成提示
print(f"所有章节下载完成！")
