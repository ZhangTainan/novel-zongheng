from flask import Flask
from flask_cors import CORS
from flask import request
from spider import *

app = Flask(__name__)
# 配置跨域
CORS(app, resources=r'/*')


@app.route('/search')
def search():
    args = request.args
    keyword = args.get('keyword', "元尊")
    pageNo = args.get('pageNo', 1)
    return search_book(keyword=keyword, pageNo=pageNo)


@app.route('/get_directory/<int:book_id>')
def directory(book_id):
    return get_directory(book_id)


@app.route('/get_content', methods=['POST'])
def content():
    url = request.json.get('url')
    return get_chapter_content(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
