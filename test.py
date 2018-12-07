#!/usr/bin/env python
import cv2
from flask import Flask, render_template, request, redirect, url_for
import base64
import numpy as np
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def t_img():
    if request.method == "POST":
        img = request.form.get("tijiao")
        img = base64.b64decode(img)
        nparr = np.fromstring(img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_RGB2BGR)
        cv2.imshow('g', img_np)
        cv2.waitKey(0)
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)