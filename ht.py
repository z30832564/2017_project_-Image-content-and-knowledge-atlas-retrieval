# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from app.search.colordescriptor import ColorDescriptor
from app.search.searcher import Searcher
from app.kg.knowledgeg import Queryer
from app.search.find_book import find_book_edge
import cv2
import base64
import numpy as np
import jieba

app = Flask(__name__)


# 主页部分
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        txt = request.form.get("content")
        print(txt)
        return redirect(url_for('search_text', string=txt))
    return render_template('index.html')


@app.route('/t_img', methods=["GET", "POST"])
def t_img():
    if request.method == "POST":
        return redirect(url_for('index_img'))
    return render_template('index.html')


@app.route('/t_text', methods=["GET", "POST"])
def t_text():
    if request.method == "POST":
        return redirect(url_for('index'))
    return render_template('index1.html')


@app.route('/index_img', methods=["GET", "POST"])
def index_img():
    if request.method == "POST":
        img = request.form.get("tijiao")
        img = base64.b64decode(img)
        nparr = np.fromstring(img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_RGB2BGR)
        find_book_edge(img_np)

        # 实例化ColorDescriptor类，bin的数量值
        cd = ColorDescriptor((8, 3, 3))

        # 提取查询图像的特征值
        features = cd.describe(img_np)
        # 实例化Searcher
        s = Searcher(features)
        s.Search()
        global results
        results = s.results
        print(results)

        return redirect(url_for('search_file'))

    return render_template('index1.html')


# 搜索页面部分
@app.route('/search_file/', methods=['POST', 'GET'])
def search_file():
    global results
    # 传递参数给html
    return render_template('result.html', results=results)


@app.route('/search_text/<string>', methods=['POST', 'GET'])
def search_text(string):
    l = list(jieba.cut_for_search(string))
    print(l)
    q = Queryer(l)
    result = q.Query()
    result.reverse()
    return render_template('result.html', results=result)