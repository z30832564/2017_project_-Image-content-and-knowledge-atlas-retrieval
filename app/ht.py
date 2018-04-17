# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from app.search.colordescriptor import ColorDescriptor
from app.search.searcher import Searcher
import jieba
from app.kg.knowledgeg import Queryer
import string
import cv2
import os

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
        image = request.files['file']
        # 保存图像
        filename = secure_filename(image.filename)
        image.save(filename)
        return redirect(url_for('search_file', filename=filename))

    return render_template('index1.html')


# 搜索页面部分
@app.route('/search_file/<filename>', methods=['POST', 'GET'])
def search_file(filename):
    query = cv2.imread(filename)
    # 实例化ColorDescriptor类，bin的数量值
    cd = ColorDescriptor((8, 3, 3))

    # 提取查询图像的特征值
    features = cd.describe(query)
    # 实例化Searcher
    s = Searcher(features)
    s.Search()
    results = s.results
    print(results)
    # 传递参数给html
    return render_template('result.html', results=results)


@app.route('/search_text/<string>', methods=['POST', 'GET'])
def search_text(string):
    # l = list(jieba.cut_for_search(string))
    l = string.split('为')
    q = Queryer(l)
    result = q.Query()
    return render_template('result.html', results=result)