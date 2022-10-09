## 这是一个纵横中文网的简单爬虫

### spider.py中封装了三个函数：

- #### 	search_book类实现了搜索关键字获取相应书的信息

- ####  get_directory实现了爬取一本书的目录章节

- ####     get_chapter_content实现了爬取某一本书某一章节的具体内容

### main.py是基于FastAPI起的接口服务，实现了上述功能的几个接口

### 接口文档地址：http://www.programerzhang.cn:8088/docs#/

### 界面如下，可以直接进行接口测试。

![image-20221009234519199](https://cdn.jsdelivr.net/gh/ZhangTainan/Drawing-bed/imgs/image-20221009234519199.png)

### flask_main.py是基于flask起的一个接口服务，实现了同样的功能。



### 请求方式和返回值类型在代码中有详细的注释。



## 使用指南

#### 1. git clone 或者下载压缩包并解压

#### 2. 执行   `pip install -r  requirements.txt` 安装依赖库

#### 3. 在项目根目录（main.py所在目录）执行一下代码启动FlaskAPI接口程序

#### 	`uvicorn main:app --host 0.0.0.0 --port 8088 --reload`

#### 	或者直接运行项目中任意一个 .py 文件



