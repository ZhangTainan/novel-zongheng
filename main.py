import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from spider import search_book, get_directory, get_chapter_content
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置允许所有端跨域
CORSMiddleware(app=app, allow_origins=["*"])


class ChapterURL(BaseModel):
    url: str
    """
    Attributes:
        url: 章节的地址
    """


@app.get("/search", tags=["搜索"])
def search(keyword: str = "元尊", pageNo: int = 1):
    """

    :param keyword: 搜索的关键字
    :param pageNo: 搜索第几页
    :return: 根据关键字搜索的结果列表
    """
    return search_book(keyword=keyword, pageNo=pageNo)


@app.get("/get_directory/{book_id}", tags=["获取某本书的章节目录"])
def get_chapters(book_id: int):
    """

    :param book_id: 小说的书号
    :return: 小说的章节列表
    """
    return get_directory(book_id)


@app.post("/get_content", tags=["获取某一章的内容"])
def get_content(data: ChapterURL):
    """

    :param data: 请求体对象
    :return: 章节内容
    """
    return get_chapter_content(url=data.url)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8088)
