import requests
from bs4 import BeautifulSoup

# 目标网页URL
url = 'http://www.baidu.com'

# 发送HTTP请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 获取网页标题
    title = soup.title.string
    print('Page Title:', title)
    
    # 获取所有段落的文本
    paragraphs = soup.find_all('p')
    for idx, paragraph in enumerate(paragraphs, start=1):
        print(f'Paragraph {idx}:', paragraph.get_text())
    print(soup)
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
