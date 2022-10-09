import requests
from bs4 import BeautifulSoup
from copyheaders import headers_raw_to_dict
import json

# 纵横中文网官网地址
BASE_URL = "https://book.zongheng.com"
# 搜索的地址
SEARCH_URL = "https://search.zongheng.com/search/book?keyword={}&sort=null&pageNo={}&pageNum={}&isFromHuayu=0"
# 获取目录的地址
DIRECTORY_URL = "https://book.zongheng.com/showchapter/{}.html"
# 获取封面图片的地址
COVER_BASE_URL = "http://static.zongheng.com/upload/"

# 从浏览器赋值的请求头
row_headers = b'''
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh,zh-CN;q=0.9,en;q=0.8
cache-control: no-cache
cookie: ZHID=2058A443F3F560E74A1DA05CAFB3B5FA; ver=2018; zh_visitTime=1665159625988; sajssdk_2015_cross_new_user=1; loginphone=13819760929; logon=NTQzNDA1NzE%3D%7CMA%3D%3D%7C%7C5Lmm5Y%2BLNjAzODMwMTQ%3D%7CdHJ1ZQ%3D%3D%7CLTM5NzA1MzU5NQ%3D%3D%7CB79BF945930B761F722AAB75F2E7EBE7; __logon__=NTQzNDA1NzE%3D%7CMA%3D%3D%7C%7C5Lmm5Y%2BLNjAzODMwMTQ%3D%7CdHJ1ZQ%3D%3D%7CLTM5NzA1MzU5NQ%3D%3D%7CB79BF945930B761F722AAB75F2E7EBE7; __zhs__=42d335a4aa125667cde89e1625111fafbc415bd289ea8b8220cbd228230312d7df3b8608287ddd8cc4c4481b3801efedde085c0d194316ac914c9c9c96a3f7a68edfac199be9c9ae170f3e27886aef9c6f7bab6b19fa16cdfef3b0f199fcc5aa32c0a1985e6f306ae2107b49cb73d02c1b54149547fa74c4b9cd84d605844965; __zhc__=30819f300d06092a864886f70d010101050003818d003081890281810096169a3b6e961507d9763a615436e49f4564bfa6ab8c577626236c959c3cd95657ef4f70f37f6a5b7320e472a1f104f343ca5dec28ec05777aa950a84d93f5530a18ddd82908735ef2ef0ee3abaf94197a7f78f30e3a4c7d83a6c408d6214665aeb567ffd5f2d36f29ddb04d22b4250b731dd00277ce37e6eb6fc987c512e8df0203010001; PassportCaptchaId=edf79c48ad1f3256759f69333a647c81; rSet=1_3_1_14_1; zhffr=www.baidu.com; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22183b33f7d2994e-054fd224b8debd-26021f51-1131564-183b33f7d2ad73%22%2C%22%24device_id%22%3A%22183b33f7d2994e-054fd224b8debd-26021f51-1131564-183b33f7d2ad73%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_c202865d524849216eea846069349eb9=1665159626,1665203758,1665211989; JSESSIONID=abcBdrT_eGwWUdDWPx2oy; Hm_lpvt_c202865d524849216eea846069349eb9=1665212011
pragma: no-cache
referer: http://book.zongheng.com/
sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: cross-site
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
'''

# 将请头处理成字典格式
headers = headers_raw_to_dict(row_headers)


# 搜索小说
def search_book(keyword: str = "灰烬领主", pageNo: int = 1, pageNum: int = 20) -> list:
    url = SEARCH_URL.format(keyword, pageNo, pageNum)
    res = requests.get(url=url, headers=headers)
    text = res.text
    json_str = json.loads(text)
    book_list = json_str["data"]["datas"]["list"]
    info_list = []
    for book in book_list:
        book_id = book["bookId"]
        book_name = book["name"]
        book_authorName = book["authorName"]
        book_cover_url = book["coverUrl"]
        book_description = book["description"]
        book_total_word = book["totalWord"]
        info_list.append({
            "id": book_id,
            "name": book_name,
            "author": book_authorName,
            "cover": COVER_BASE_URL + book_cover_url,
            "description": book_description,
            "words": book_total_word
        })

    return info_list


# 获取章节目录
def get_directory(book_id: int) -> list:
    url = DIRECTORY_URL.format(book_id)
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    ul_element = soup.select_one("body > div.container > div:nth-child(2) > div.volume-list > div:nth-child(2) > ul")
    if not ul_element:
        ul_element = soup.select_one("body > div.container > div:nth-child(2) > div.volume-list > div > ul")
    li_elements = ul_element.find_all("li")
    chapter_list = []
    for li in li_elements:
        a = li.find("a")
        chapter_name = a.text
        chapter_url = a["href"]
        chapter_list.append({
            "name": chapter_name,
            "url": chapter_url
        })
    return chapter_list


# 获取某一章节的内容
def get_chapter_content(url: str) -> dict:
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select_one("#readerFt > div > div.reader_box > div.title > div.title_txtbox").text
    content = soup.select_one("#readerFt > div > div.reader_box > div.content").text
    return {
        "title": title,
        "content": content
    }


if __name__ == '__main__':
    print(len(search_book("天")))
    print(get_directory(1217041))
    print(get_chapter_content("https://book.zongheng.com/chapter/1215587/68240827.html"))
