# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from app.search.colordescriptor import ColorDescriptor
from app.search.searcher import Searcher

import cv2
import os

app = Flask(__name__)


# 主页部分
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files['file']
        # 保存图像
        filename = secure_filename(image.filename)
        image.save(filename)

        return redirect(url_for('search', filename=filename))

    return render_template('index.html')


# 搜索页面部分
@app.route('/searchs/<filename>', methods=['POST', 'GET'])
def search(filename):
    query = cv2.imread(filename)
    # 实例化ColorDescriptor类，bin的数量值
    cd = ColorDescriptor((8, 3, 3))

    # 提取查询图像的特征值
    features = cd.describe(query)
    # 实例化Searcher
    s = Searcher(features)
    s.Search()
    results = s.results
    # 传递参数给html
    return render_template('result.html', results=results, filename=filename)
