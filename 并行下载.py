from bs4 import BeautifulSoup
import requests, os
from concurrent.futures import ThreadPoolExecutor

# 配置参数
BASE_URL = "https://www.ireader.com/index.php?ca=Chapter.Index&pca=bookdetail.index&bid=11753596&cid="
PARALLEL_COUNT = 100  # 并行下载数量，可根据需要调整
MAX_RETRY = 3  # 单个章节最大重试次数
START_CID = 1  # 起始章节ID

# 获取书名
r = requests.get(BASE_URL + "1")
book_title = BeautifulSoup(r.text, 'html.parser').select_one('i a').get_text()
os.makedirs(book_title, exist_ok=True)
print(f"书名：{book_title}")

# 下载函数（带重试机制）
def download_chapter(cid):
    for attempt in range(MAX_RETRY):
        try:
            # 获取并解析章节内容
            response = requests.get(BASE_URL + str(cid))
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查章节是否存在
            article = soup.find('div', class_='article')
            if not article:
                return f"章节 {cid} 不存在"
                
            # 提取标题和内容
            title = article.find('h2').get_text().strip()
            content = "\n".join(p.get_text() for p in article.find_all('p'))
            
            # 保存文件
            with open(f"{book_title}/{cid}.{title}.txt", 'w', encoding='utf-8') as f:
            # with open(f"{book_title}/{title}.txt", 'w', encoding='utf-8') as f:
                f.write(content)
                
            return f"章节 {cid} 下载成功: {title}"
            
        except Exception as e:
            if attempt < MAX_RETRY - 1:
                continue  # 重试
            return f"章节 {cid} 下载失败: {str(e)}"
    return f"章节 {cid} 下载失败"

# 使用线程池并行下载
with ThreadPoolExecutor(max_workers=PARALLEL_COUNT) as executor:
    cid = START_CID
    while True:
        # 提交一批下载任务
        futures = [executor.submit(download_chapter, cid + i) for i in range(PARALLEL_COUNT)]
        results = [future.result() for future in futures]
        
        # 打印结果并检查是否结束
        all_failed = True
        for result in results:
            print(result)
            if "成功" in result:
                all_failed = False
        
        # 如果全部失败则退出
        if all_failed:
            break
            
        cid += PARALLEL_COUNT

print("所有章节下载完成")
